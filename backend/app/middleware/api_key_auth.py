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

async def verify_api_key(x_api_key: str = Header(...)) -> None:
    """
    Security check that validates an 'X-API-Key' header.
    
    If the key is missing or incorrect, it immediately blocks the request 
    and sends back a 401 Unauthorized response.
    """
    # 'compare_digest' is a security best practice that prevents hackers from 
    # guessing keys by measuring how long the comparison takes.
    if not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized: Access to this endpoint requires a valid API key."
        )
