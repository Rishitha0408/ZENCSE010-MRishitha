import unittest
from unittest.mock import AsyncMock, patch
import datetime
import base64
from app.models.certificate import Recipient, CertificateDetails
from app.schemas.certificate import IssueCertificateRequest
from app.services.certificate_service import issue_certificate
from io import BytesIO

class TestCertificateService(unittest.IsolatedAsyncioTestCase):
    async def test_issue_certificate(self):
        # Setup mock db
        mock_db = AsyncMock()
        mock_db.certificates.insert_one = AsyncMock(return_value=None)
        
        # Test request
        req = IssueCertificateRequest(
            recipient=Recipient(name="Alice", email="alice@example.com", student_id="123"),
            certificate=CertificateDetails(title="DevOps Expert", description="Passed DevOps course", skills=["Docker"])
        )
        
        # Call the service
        result = await issue_certificate(req, mock_db)
        
        # Verify db insert was called once
        mock_db.certificates.insert_one.assert_called_once()
        
        # Check return structure
        self.assertTrue(result["certificate_id"].startswith("CERT-"))
        self.assertIn("qr_code_base64", result)
        self.assertIn("qr_code_url", result)
        self.assertIn("linkedin_share_url", result)
        self.assertIn("issued_at", result)
        self.assertEqual(result["status"], "ACTIVE")
        
        # Ensure QR generated correctly (PNG)
        decoded_qr = base64.b64decode(result["qr_code_base64"])
        self.assertTrue(decoded_qr.startswith(b'\x89PNG\r\n\x1a\n'))
        
        # LinkedIn URL check
        self.assertTrue("linkedin.com/profile/add" in result["linkedin_share_url"])
        self.assertTrue("DevOps+Expert" in result["linkedin_share_url"] or "DevOps%20Expert" in result["linkedin_share_url"])

    async def test_get_certificate(self):
        # Setup mock db
        mock_db = AsyncMock()
        mock_doc = {"certificate_id": "CERT-123", "status": "ACTIVE"}
        mock_db.certificates.find_one = AsyncMock(return_value=mock_doc)

        from app.services.certificate_service import get_certificate
        result = await get_certificate("CERT-123", mock_db)

        # Verify db find_one was called correctly
        mock_db.certificates.find_one.assert_called_once_with({"certificate_id": "CERT-123"}, {"_id": 0})
        
        # Check return
        self.assertEqual(result, mock_doc)

    async def test_list_certificates(self):
        # Setup mock db
        from unittest.mock import MagicMock
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # We need to mock the cursor chain: find().sort().skip().limit().to_list()
        mock_db.certificates.find.return_value = mock_cursor
        mock_cursor.sort.return_value = mock_cursor
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_docs = [{"certificate_id": "CERT-1"}, {"certificate_id": "CERT-2"}]
        mock_cursor.to_list = AsyncMock(return_value=mock_docs)

        from app.services.certificate_service import list_certificates
        import pymongo
        
        result = await list_certificates(mock_db, skip=0, limit=20)
        
        # Assertions on the chain
        mock_db.certificates.find.assert_called_once_with({}, {"_id": 0})
        mock_cursor.sort.assert_called_once_with("issued_at", pymongo.DESCENDING)
        mock_cursor.skip.assert_called_once_with(0)
        mock_cursor.limit.assert_called_once_with(20)
        mock_cursor.to_list.assert_called_once_with(length=20)
        
        # Check return
        self.assertEqual(result, mock_docs)

    async def test_revoke_certificate(self):
        # Setup mock db
        mock_db = AsyncMock()
        mock_result = AsyncMock()
        mock_result.modified_count = 1
        mock_db.certificates.update_one = AsyncMock(return_value=mock_result)

        from app.services.certificate_service import revoke_certificate
        
        result = await revoke_certificate("CERT-123", mock_db, "Mistake", "AdminUser")
        
        self.assertTrue(result)
        mock_db.certificates.update_one.assert_called_once()
        call_args = mock_db.certificates.update_one.call_args[0]
        self.assertEqual(call_args[0], {"certificate_id": "CERT-123"})
        self.assertEqual(call_args[1]["$set"]["status"], "REVOKED")
        self.assertEqual(call_args[1]["$set"]["revocation"]["reason"], "Mistake")
        self.assertEqual(call_args[1]["$set"]["revocation"]["revokedBy"], "AdminUser")
        self.assertIn("revokedAt", call_args[1]["$set"]["revocation"])

    async def test_revoke_certificate_not_found(self):
        mock_db = AsyncMock()
        mock_result = AsyncMock()
        mock_result.modified_count = 0
        mock_db.certificates.update_one = AsyncMock(return_value=mock_result)

        from app.services.certificate_service import revoke_certificate
        
        result = await revoke_certificate("CERT-999", mock_db, "Mistake", "AdminUser")
        
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
