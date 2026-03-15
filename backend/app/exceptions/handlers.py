"""
Centralized Exception and Error Handlers

This module establishes how our application responds when things go wrong. 
Instead of crashing or sending confusing technical traces to the user, we 
catch errors and translate them into clean, standardized JSON responses.
"""

# 'FastAPI' components for managing requests and sending structured JSON responses.
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
# 'traceback' is used for internal logging to help developers see exactly where an error occurred.
import traceback

class CertificateNotFoundException(Exception):
    """A custom error specifically used when a requested certificate ID does not exist."""
    def __init__(self, certificate_id: str):
        self.certificate_id = certificate_id

async def certificate_not_found_handler(request: Request, exc: CertificateNotFoundException):
    """Translates a 'Missing Certificate' error into a friendly 404 Not Found response."""
    return JSONResponse(
        status_code=404, 
        content={
            "error": "Certificate not found",
            "certificate_id": exc.certificate_id
        }
    )

async def validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Handles 'Mismatch' errors when the user sends data that doesn't follow our model rules.
    It provides a 422 Unprocessable Entity response with details on exactly which fields are wrong.
    """
    return JSONResponse(
        status_code=422, 
        content={
            "error": "Validation failed",
            "details": exc.errors()
        }
    )

async def generic_error_handler(request: Request, exc: Exception):
    """
    The safety net: Handles any unexpected crashes or errors (500 Internal Server Error).
    It logs the full error traceback for the developers but keeps the user response clean.
    """
    # Print the full technical error to the server console for debugging.
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500, 
        content={
            "error": "Internal server error"
        }
    )
