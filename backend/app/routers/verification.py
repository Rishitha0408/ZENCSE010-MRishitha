"""
Verification Router Module

This module defines the public verification endpoint. It's the destination for 
QR code scans and manual ID lookups. Verification logic is designed to be 
very fast and highly reliable.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, Request
from app.database import get_db
from app.services.verification_service import verify_certificate_logic
from app.services.linkedin_service import generate_linkedin_share_url
from app.middleware.rate_limiter import limiter

from app.schemas.verification import VerificationResult

router = APIRouter()

@router.get("/{certificate_id}", response_model=VerificationResult)
@limiter.limit("60/minute")
async def verify_certificate_endpoint(
    request: Request,
    certificate_id: str,
    db=Depends(get_db)
):
    """
    Publicly checks the authenticity and status of a certificate.
    Always returns 200 OK with the result status.
    """
    client_ip = request.client.host
    
    # The service already handles logging and returns formatted result.
    raw_result = await verify_certificate_logic(certificate_id, client_ip, db)
    
    # Map the service result to the Schema
    # The service returns a dict. We need to ensure it matches VerificationResult.
    
    cert_data = raw_result.get("data", {})
    
    return VerificationResult(
        result=raw_result["status"],
        certificate_id=certificate_id,
        recipient_name=cert_data.get("recipient", {}).get("name"),
        course_title=cert_data.get("certificate", {}).get("title"),
        issued_at=cert_data.get("issued_at"),
        expires_at=None, # Add logic for expiry if needed
        institution_name="CertShield Institution", # Default or from config
        verified_at=raw_result["verified_at"],
        message=raw_result["message"],
        linkedin_share_url=generate_linkedin_share_url(
            cert_id=certificate_id,
            title=cert_data.get("certificate", {}).get("title"),
            issued_at=cert_data.get("issued_at") if isinstance(cert_data.get("issued_at"), datetime) else datetime.fromisoformat(cert_data.get("issued_at")),
            institution_name="CertShield Institution"
        ) if raw_result["status"] == "VALID" else None
    )
