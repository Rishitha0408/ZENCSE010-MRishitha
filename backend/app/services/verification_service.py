"""
Certificate Verification Service

This module handles the logic for verifying certificates. It checks the 
cryptographic signature to ensure data integrity and queries the database 
to verify the certificate's current status (Active vs Revoked).
"""

from datetime import datetime, timezone
from app.services.signature_service import verify_certificate
from app.services.certificate_service import get_certificate
from app.models.verification_log import VerificationLog

async def verify_certificate_logic(certificate_id: str, client_ip: str, db) -> dict:
    """
    Orchestrates the verification process for a single certificate and logs the attempt.
    """
    
    # STEP 1: Look up the certificate in the database.
    cert_doc = await get_certificate(certificate_id, db)
    
    if not cert_doc:
        # LOGGING: Record the failed attempt (Not Found).
        log = VerificationLog(
            certificate_id=certificate_id,
            result="NOT_FOUND",
            client_ip=client_ip
        )
        await db.verification_logs.insert_one(log.model_dump())
        
        return {
            "is_valid": False,
            "status": "NOT_FOUND",
            "message": "No certificate found with the provided ID.",
            "verified_at": log.verified_at,
            "certificate_id": certificate_id
        }

    # STEP 2: Verify the Cryptographic Signature.
    # We rebuild the signed data package to check for tampering.
    data_to_verify = {
        "certificate_id": cert_doc["certificate_id"],
        "recipient": cert_doc["recipient"],
        "certificate": cert_doc["certificate"],
        "issued_at": cert_doc["issued_at"].isoformat() if isinstance(cert_doc["issued_at"], datetime) else cert_doc["issued_at"]
    }
    
    is_authentic = verify_certificate(data_to_verify, cert_doc["signature"]["value"])
    
    if not is_authentic:
        # LOGGING: Record the security failure (Tampered).
        log = VerificationLog(
            certificate_id=certificate_id,
            result="TAMPERED",
            client_ip=client_ip
        )
        await db.verification_logs.insert_one(log.model_dump())
        
        return {
            "is_valid": False,
            "status": "TAMPERED",
            "message": "Warning: The certificate data appears to have been altered!",
            "verified_at": log.verified_at,
            "certificate_id": certificate_id
        }

    # STEP 3: Check the Revocation Status.
    if cert_doc["status"] == "REVOKED":
        # LOGGING: Record the check of a revoked certificate.
        log = VerificationLog(
            certificate_id=certificate_id,
            result="REVOKED",
            client_ip=client_ip
        )
        await db.verification_logs.insert_one(log.model_dump())
        
        return {
            "is_valid": False,
            "status": "REVOKED",
            "message": f"This certificate was revoked on {cert_doc['revocation']['revokedAt']}.",
            "reason": cert_doc['revocation']['reason'],
            "verified_at": log.verified_at,
            "certificate_id": certificate_id
        }

    # SUCCESS: The certificate is both authentic and active.
    log = VerificationLog(
        certificate_id=certificate_id,
        result="VALID",
        client_ip=client_ip
    )
    
    # Update verification stats on the certificate record.
    await db.certificates.update_one(
        {"certificate_id": certificate_id},
        {
            "$inc": {"verification_count": 1},
            "$set": {"last_verified_at": log.verified_at}
        }
    )
    # Save the success log.
    await db.verification_logs.insert_one(log.model_dump())

    return {
        "is_valid": True,
        "status": "VALID",
        "message": "Certificate verified successfully. This credential is authentic.",
        "verified_at": log.verified_at,
        "certificate_id": certificate_id,
        "data": cert_doc
    }
