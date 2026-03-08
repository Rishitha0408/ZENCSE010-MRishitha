"""
Verification Router Module

This module defines the public verification endpoint. It's the destination for 
QR code scans and manual ID lookups. Verification logic is designed to be 
very fast and highly reliable.
"""

from fastapi import APIRouter, Depends, Request
from app.database import get_db
from app.services.verification_service import verify_certificate_logic
from app.middleware.rate_limiter import limiter

router = APIRouter()

@router.get("/{certificate_id}")
@limiter.limit("30/minute") # Restrict usage to prevent brute-force 'fishing' for valid IDs.
async def verify_certificate_endpoint(
    request: Request,
    certificate_id: str,
    db=Depends(get_db)
):
    """
    Publicly checks the authenticity and status of a certificate.
    Returns: A verification report including validity status and original data.
    """
    
    # Extract the client's IP address to log who is performing the check.
    client_ip = request.client.host
    
    # Run the verification services and gather the report.
    result = await verify_certificate_logic(certificate_id, client_ip, db)
    
    return result
