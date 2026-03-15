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
    result: Literal["VALID", "REVOKED", "TAMPERED", "NOT_FOUND"]
    certificate_id: str
    recipient_name: Optional[str] = None
    course_title: Optional[str] = None
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    institution_name: Optional[str] = None
    verified_at: datetime
    message: str
    linkedin_share_url: Optional[str] = None
