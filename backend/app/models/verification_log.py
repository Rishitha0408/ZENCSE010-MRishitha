"""
Verification Log Model

This module defines the structure for logging every attempt to verify a certificate.
Auditing these attempts helps us detect potential fraud and track the reach 
of the issued credentials.
"""

# 'pydantic' is used for structured, validated data modeling.
from pydantic import BaseModel, Field
# 'typing' allows us to specify allowed values for the verification result.
from typing import Literal
# 'datetime' records the exact second the verification happened.
from datetime import datetime, timezone

class VerificationLog(BaseModel):
    """
    The blueprint for a single verification audit record.
    Every time someone scans a QR code or enters a certificate ID, we save one of these.
    """
    
    # The ID of the certificate that was being checked.
    certificate_id: str
    
    # What was the outcome of the check?
    # - VALID: Verification passed.
    # - REVOKED: Certificate exists but has been invalidated.
    # - TAMPERED: Digital signature check failed (data was altered).
    # - NOT_FOUND: No certificate exists with this ID.
    result: Literal["VALID", "REVOKED", "TAMPERED", "NOT_FOUND"]
    
    # Precise timestamp of the verification attempt.
    verified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # The network address of the person verifying the certificate (useful for fraud detection).
    client_ip: str
