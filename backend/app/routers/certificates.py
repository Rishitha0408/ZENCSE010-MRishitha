"""
Certificates Router Module

This module defines the public-facing API endpoints for certificate interactions.
Users can use these routes to retrieve or list available certificates.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, Request, Response
from app.database import get_db
from app.services.certificate_service import (
    get_certificate, 
    list_certificates, 
    issue_certificate, 
    revoke_certificate,
    get_qr_code_binary
)
from app.schemas.certificate import CertificateCreateRequest, CertificateResponse, CertificateListItem
from app.middleware.rate_limiter import limiter
from app.middleware.api_key_auth import verify_api_key

# All routes in this router require a valid API key.
router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.get("/", response_model=list[CertificateListItem])
@limiter.limit("20/minute") # Protect this browse endpoint from excessive automated scaping.
async def get_all_certificates(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db=Depends(get_db)
):
    """Retrieves a paginated list of certificates."""
    # Fetch results from the certificate business logic service.
    return await list_certificates(db, skip, limit)

@router.post("/", status_code=201, response_model=CertificateResponse)
@limiter.limit("10/minute")
async def issue_new_certificate(
    request: Request,
    cert_request: CertificateCreateRequest,
    db=Depends(get_db)
):
    """Issue a new certificate."""
    # Convert new schema to internal model if necessary, or update service to handle it
    # For now, let's assume service is updated or we map it here
    from app.models.certificate import Recipient, CertificateDetails
    
    # Mapping CertificateCreateRequest to the expected format of issue_certificate
    class MockRequest:
        def __init__(self, recipient, certificate):
            self.recipient = recipient
            self.certificate = certificate
            
    legacy_request = MockRequest(
        recipient=Recipient(
            name=cert_request.recipient_name,
            email=cert_request.recipient_email,
            student_id=cert_request.recipient_student_id or "N/A"
        ),
        certificate=CertificateDetails(
            title=cert_request.course_title,
            description=cert_request.description or f"Certificate for {cert_request.course_title}",
            skills=cert_request.skills
        )
    )
    
    return await issue_certificate(legacy_request, db)

@router.get("/{certificate_id}", response_model=dict)
@limiter.limit("60/minute") # Allow more frequent lookups for individual certificates.
async def get_certificate_by_id(
    request: Request,
    certificate_id: str,
    db=Depends(get_db)
):
    """Get certificate detail."""
    # Look up the certificate document through the service.
    cert = await get_certificate(certificate_id, db)
    
    if not cert:
        # If the search comes up empty, tell the user exactly which IDs were missing.
        raise HTTPException(
            status_code=404, 
            detail=f"Certificate not found" # Handled by custom exception if we use it
        )
        
    return cert

@router.put("/{certificate_id}/revoke")
@limiter.limit("5/minute")
async def revoke_existing_certificate(
    request: Request,
    certificate_id: str,
    db=Depends(get_db)
):
    """Revoke a certificate."""
    success = await revoke_certificate(certificate_id, db)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail=f"Certificate not found"
        )
    return {"status": "success", "message": "Certificate revoked successfully"}

@router.get("/{certificate_id}/qrcode")
@limiter.limit("30/minute")
async def get_certificate_qrcode(
    request: Request,
    certificate_id: str,
    db=Depends(get_db)
):
    """Returns QR code image as binary PNG."""
    qr_bytes = await get_qr_code_binary(certificate_id, db)
    if not qr_bytes:
        raise HTTPException(status_code=404, detail="Certificate not found")
        
    return Response(content=qr_bytes, media_type="image/png")
