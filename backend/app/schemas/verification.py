"""
Verification Schema Module

This module defines the structure for data returned during certificate verification.
It ensures that the verification results are clear and consistent for the client.
"""

from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class VerificationResult(BaseModel):
    """
    The structured response for a certificate verification check.
    """
    
    # Is the certificate authentic and valid?
    is_valid: bool
    
    # The current status: VALID, REVOKED, or TAMPERED.
    status: Literal["VALID", "REVOKED", "TAMPERED", "NOT_FOUND"]
    
    # Optional message explaining the verification result.
    message: str
    
    # The time the verification was performed.
    verified_at: datetime
    
    # The certificate ID that was checked.
    certificate_id: str
