import unittest
from app.services.signature_service import sign_certificate, verify_certificate

class TestSignatureService(unittest.TestCase):
    def test_sign_and_verify_roundtrip(self):
        """Test that a signed certificate can be verified successfully."""
        data = {
            "student_name": "John Doe",
            "course": "Computer Science",
            "grade": "A",
            "issue_date": "2023-10-27"
        }
        
        # Sign the data
        signature_b64, data_hash = sign_certificate(data)
        
        # Verify the signature
        is_valid = verify_certificate(data, signature_b64)
        self.assertTrue(is_valid, "Signature should be valid for unmodified data")

    def test_verify_modified_data_fails(self):
        """Test that modifying a single field results in a verification failure."""
        data = {
            "student_name": "John Doe",
            "course": "Computer Science",
            "grade": "A",
            "issue_date": "2023-10-27"
        }
        
        # Sign the original data
        signature_b64, data_hash = sign_certificate(data)
        
        # Modify the data
        tampered_data = data.copy()
        tampered_data["grade"] = "A+"
        
        # Verify with tampered data
        is_valid = verify_certificate(tampered_data, signature_b64)
        self.assertFalse(is_valid, "Signature should be invalid when data is modified")

    def test_verify_malformed_signature_fails(self):
        """Test that a malformed signature returns False."""
        data = {"key": "value"}
        signature_b64, _ = sign_certificate(data)
        
        # Mess up the signature
        bad_sig = signature_b64[:-5] + "XXXXX"
        
        is_valid = verify_certificate(data, bad_sig)
        self.assertFalse(is_valid, "Signature should be invalid for a malformed signature")
        
        # completely invalid base64
        self.assertFalse(verify_certificate(data, "not-base64-!@#$"))

if __name__ == '__main__':
    unittest.main()
