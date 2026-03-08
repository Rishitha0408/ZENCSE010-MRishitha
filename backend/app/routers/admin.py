"""
Admin Router Module

This module defines restricted API routes that only authorized systems or 
administrators can access. This includes the ability to issue new certificates 
and revoke existing ones if needed.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from app.database import get_db
from app.services.certificate_service import issue_certificate, revoke_certificate
from app.schemas.certificate import IssueCertificateRequest
from app.middleware.api_key_auth import verify_api_key
from app.middleware.rate_limiter import limiter

# All routes in this router will require a valid API key for authentication.
router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.post("/issue")
@limiter.limit("10/minute") # Heavily restricted to prevent abuse of the cryptographic keys.
async def issue_new_certificate(
    request: Request,
    cert_request: IssueCertificateRequest,
    db=Depends(get_db)
):
    """
    Secure endpoint to create a new, digitally signed certificate.
    """
    # Delegate the complex creation and signing process to our service layer.
    return await issue_certificate(cert_request, db)

@router.post("/revoke/{certificate_id}")
@limiter.limit("5/minute") # Revocation is a critical action and is highly restricted.
async def revoke_existing_certificate(
    request: Request,
    certificate_id: str,
    reason: str,
    revoked_by: str,
    db=Depends(get_db)
):
    """
    Mark a certificate as 'REVOKED' to prevent further verification.
    """
    # Attempt to update the status in the database through the service layer.
    success = await revoke_certificate(certificate_id, reason, revoked_by, db)
    
    if not success:
        # If the update had zero effect, it means the ID was probably incorrect.
        raise HTTPException(
            status_code=404, 
            detail=f"Could not revoke: The ID '{certificate_id}' does not exist."
        )
        
    return {"status": "success", "message": f"The certificate '{certificate_id}' has been revoked successfully."}
