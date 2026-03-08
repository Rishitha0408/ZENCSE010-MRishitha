"""
Certificate Data Models

This module defines the blueprint (schema) for how certificate data is stored 
and structured. We use Pydantic models to ensure data validation, meaning the 
system will automatically reject any data that doesn't follow these rules.
"""

# 'pydantic' allows us to create structured data models with automatic validation.
from pydantic import BaseModel, Field
# 'typing' provides type hints to make the code easier to read and debug.
from typing import Optional, List, Literal
# 'datetime' is used for recording precisely when certificates were issued or verified.
from datetime import datetime, timezone
# 'uuid' allows us to generate globally unique identifiers for each certificate.
import uuid

def generate_cert_id():
    """
    Generates a unique human-friendly ID for a certificate.
    Example: 'CERT-550e8400-e29b-41d4-a716-446655440000'
    """
    return f"CERT-{uuid.uuid4()}"

class Recipient(BaseModel):
    """Information about the person receiving the certificate."""
    name: str # Full name of the student.
    email: str # Contact email address.
    student_id: str # Unique internal ID for the student.

class CertificateDetails(BaseModel):
    """Specific details about what the certificate represents."""
    title: str # e.g., 'Master of Blockchain'
    description: str # A brief summary of the achievement.
    skills: List[str] # A list of specific competencies gained.

class Signature(BaseModel):
    """Cryptographic proof that makes the certificate tamper-proof."""
    algorithm: str # The hashing/signing algorithm used (e.g., ECDSA_P256).
    key_id: str # The ID of the key used (allows for key rotation).
    value: str # The actual digital signature string.
    data_hash: str # The original 'fingerprint' of the data that was signed.

class QR(BaseModel):
    """Metadata for the QR code embedded on the certificate."""
    url: str # The direct link to the verification page.
    generated_at: datetime # When the QR code was created.

class Revocation(BaseModel):
    """Details recorded if a certificate is ever invalidated."""
    revokedAt: datetime # Timestamp of revocation.
    reason: str # Why it was revoked (e.g., 'Issued in error').
    revokedBy: str # The admin user who performed the action.

class CertificateDocument(BaseModel):
    """
    The complete 'Source of Truth' document for a certificate.
    This model combines all the sub-models above into a single structure stored in MongoDB.
    """
    # A unique prefix-tagged ID for the certificate.
    certificate_id: str = Field(default_factory=generate_cert_id)
    
    # Recipient and academic details.
    recipient: Recipient
    certificate: CertificateDetails
    
    # Lifecycle timestamps.
    issued_at: datetime
    expires_at: Optional[datetime] = None
    
    # Security and Verification components.
    signature: Signature
    qr: QR
    
    # Current status of the certificate.
    status: Literal["ACTIVE", "REVOKED", "EXPIRED"] = Field(default="ACTIVE")
    
    # Optional revocation details if the certificate is no longer valid.
    revocation: Optional[Revocation] = None
    
    # Analytics for how many times this certificate has been checked.
    verification_count: int = Field(default=0)
    last_verified_at: Optional[datetime] = None
    
    # System metadata for the record itself.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
