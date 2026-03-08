"""
Certificates Router Module

This module defines the public-facing API endpoints for certificate interactions.
Users can use these routes to retrieve or list available certificates.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, Request
from app.database import get_db
from app.services.certificate_service import get_certificate, list_certificates
from app.middleware.rate_limiter import limiter

# Creating a standard router with a prefix of '/certificates'.
router = APIRouter()

@router.get("/")
@limiter.limit("20/minute") # Protect this browse endpoint from excessive automated scaping.
async def get_all_certificates(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db=Depends(get_db)
):
    """
    Retrieves a paginated list of certificates.
    
    Defaults:
    - skips: 0 (start from the beginning)
    - limit: 20 (return 20 certificates per page)
    """
    # Fetch results from the certificate business logic service.
    return await list_certificates(db, skip, limit)

@router.get("/{certificate_id}")
@limiter.limit("60/minute") # Allow more frequent lookups for individual certificates.
async def get_certificate_by_id(
    request: Request,
    certificate_id: str,
    db=Depends(get_db)
):
    """
    Search for a single certificate using its unique ID.
    If not found, it sends a 404 (Not Found) error back.
    """
    # Look up the certificate document through the service.
    cert = await get_certificate(certificate_id, db)
    
    if not cert:
        # If the search comes up empty, tell the user exactly which IDs were missing.
        raise HTTPException(
            status_code=404, 
            detail=f"The certificate ID '{certificate_id}' was not found in our records."
        )
        
    return cert
