"""
Certificate Business Logic Service

This is the orchestration layer where different system components (database, 
cryptography, and QR generation) are combined to perform complex operations 
like issuing, retrieving, or revoking certificates.
"""

# 'datetime' is used for recording precisely when certificates were issued or revoked.
import datetime
# 'urllib.parse' allows us to safely encode text into URLs (e.g., for the LinkedIn share button).
import urllib.parse
# 'pymongo' is used here specifically for defining index sort directions (e.g., DESCENDING).
import pymongo

# Internal local modules for data models, security, and utility services.
from app.models.certificate import CertificateDocument, Signature, QR, generate_cert_id
from app.services.signature_service import sign_certificate
from app.services.qr_service import generate_qr_base64
from app.services.linkedin_service import generate_linkedin_share_url
from app.config import settings

async def issue_certificate(request, db):
    """
    Main workflow for creating a new digital certificate.
    
    The Process:
    1. Generate a unique ID and timestamp.
    2. Electronically sign the data to make it tamper-proof.
    3. Generate a QR code for easy physical verification.
    4. Save the whole package to the database.
    5. Construct a LinkedIn 'Add to Profile' link for the student.
    """
    # STEP 1: Identification.
    cert_id = generate_cert_id()
    issued_at = datetime.datetime.now(datetime.timezone.utc)
    
    # STEP 2: Tamper-Proofing.
    # We collect the core certificate information into a dictionary to be digitally signed.
    data_to_sign = {
        "certificate_id": cert_id,
        "recipient": request.recipient.model_dump(),
        "certificate": request.certificate.model_dump(),
        "issued_at": issued_at.isoformat()
    }
    # Create the cryptographic signature and a unique data hash (fingerprint).
    signature_b64, data_hash = sign_certificate(data_to_sign)
    
    # STEP 3: Scannability.
    # Create the verification URL and its corresponding QR code image.
    verify_url = f"{settings.verify_base_url}/{cert_id}"
    qr_b64 = generate_qr_base64(verify_url)
    
    # STEP 4: Data Assembly.
    # Combine all pieces into the final CertificateDocument model.
    cert_doc = CertificateDocument(
        certificate_id=cert_id,
        recipient=request.recipient,
        certificate=request.certificate,
        issued_at=issued_at,
        signature=Signature(
            algorithm="ECDSA_P256_SHA256",
            key_id="default",
            value=signature_b64,
            data_hash=data_hash
        ),
        qr=QR(
            url=verify_url,
            generated_at=issued_at
        )
    )
    
    # STEP 5: Persistence.
    # Save the document to our MongoDB 'certificates' collection.
    await db.certificates.insert_one(cert_doc.model_dump())
    
    # STEP 6: Student Social Proof.
    linkedin_share_url = generate_linkedin_share_url(
        cert_id=cert_id,
        title=request.certificate.title,
        issued_at=issued_at,
        institution_name="Your Institution" # Could be from settings
    )
    
    # Return the clean summary response for the API.
    return {
        "certificate_id": cert_id,
        "qr_code_base64": qr_b64,
        "qr_code_url": verify_url,
        "linkedin_share_url": linkedin_share_url,
        "issued_at": issued_at.isoformat(),
        "status": cert_doc.status
    }

async def get_certificate(certificate_id: str, db) -> dict | None:
    """
    Search functionality to find a specific certificate by its unique ID.
    Returns the document if found, or None if it doesn't exist.
    """
    # 'find_one' stops searching once it finds a match, maximizing efficiency.
    # '{"_id": 0}' prevents MongoDB's internal technical ID from being returned.
    return await db.certificates.find_one({"certificate_id": certificate_id}, {"_id": 0})

async def list_certificates(db, skip: int = 0, limit: int = 20) -> list[dict]:
    """
    Retrieves a list of certificates with pagination.
    """
    # Use 'issued_at' or 'created_at'? The previous code used 'created_at'.
    # Checking what's in the document. CertificateDocument has 'issued_at'.
    cursor = db.certificates.find({}, {"_id": 0}).sort("issued_at", pymongo.DESCENDING).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def revoke_certificate(certificate_id: str, db, reason: str = "Revoked by admin", revoked_by: str = "admin") -> bool:
    """
    Invalidates an existing certificate.
    """
    revoked_at = datetime.datetime.now(datetime.timezone.utc)
    
    result = await db.certificates.update_one(
        {"certificate_id": certificate_id},
        {"$set": {
            "status": "REVOKED",
            "revocation": {
                "revokedAt": revoked_at,
                "reason": reason,
                "revokedBy": revoked_by
            }
        }}
    )
    
    return result.modified_count > 0

async def get_stats(db) -> dict:
    """
    Returns summary statistics for the dashboard.
    """
    total = await db.certificates.count_documents({})
    active = await db.certificates.count_documents({"status": "ACTIVE"})
    revoked = await db.certificates.count_documents({"status": "REVOKED"})
    
    # Verifications today (UTC)
    from app.services.verification_service import get_verifications_count_today
    verifications_today = await get_verifications_count_today(db)
    
    return {
        "total": total,
        "active": active,
        "revoked": revoked,
        "verifications_today": verifications_today
    }

async def get_qr_code_binary(certificate_id: str, db) -> bytes | None:
    """
    Returns the QR code image as raw bytes (PNG).
    """
    cert = await get_certificate(certificate_id, db)
    if not cert:
        return None
        
    verify_url = cert["qr"]["url"]
    from app.services.qr_service import generate_qr_binary
    return generate_qr_binary(verify_url)
