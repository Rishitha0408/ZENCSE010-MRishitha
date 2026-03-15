"""
Admin Router Module

This module defines restricted API routes that only authorized systems or 
administrators can access. This includes the ability to issue new certificates 
and revoke existing ones if needed.
"""

from fastapi import APIRouter, Depends, Request
from app.database import get_db
from app.services.certificate_service import get_stats
from app.middleware.api_key_auth import verify_api_key
from app.middleware.rate_limiter import limiter

# All routes in this router require a valid API key for authentication.
router = APIRouter(prefix="/stats", dependencies=[Depends(verify_api_key)])

@router.get("/")
@limiter.limit("20/minute")
async def get_dashboard_stats(
    request: Request,
    db=Depends(get_db)
):
    """Returns total, active, revoked, and today's verifications."""
    return await get_stats(db)
