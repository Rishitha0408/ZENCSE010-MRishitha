"""
API Key Authentication Middleware

This module provides a gatekeeping mechanism. It ensures that only authorized 
administrators with a valid secret key can access sensitive parts of the application.
"""

# 'secrets' provides tools for securely comparing passwords or keys to prevent "timing attacks."
import secrets
# 'fastapi' components to read headers from incoming requests and raise security errors.
from fastapi import Header, HTTPException
# 'app.config' contains the expected API key we compare against.
from app.config import settings

from typing import Optional

async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    """
    Security check that validates an 'X-API-Key' header.
    
    If the key is missing or incorrect, it immediately blocks the request 
    and sends back a 401 Unauthorized response.
    """
    # If the key is missing or doesn't match, return 401 (Satisfies US-16)
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=401, 
            detail="Invalid API Key"
        )
