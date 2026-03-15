"""
API Request Schemas

This module defines 'Schemas', which act as strict protocols for what data 
a user is allowed to send to the API. Unlike 'Models' (which describe stored data), 
these focus specifically on the input received from the outside world.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime

class CertificateCreateRequest(BaseModel):
    recipient_name: str
    recipient_email: EmailStr
    recipient_student_id: Optional[str] = None
    course_title: str
    description: Optional[str] = None
    skills: List[str] = []
    issue_date: date
    expiry_date: Optional[date] = None

class CertificateResponse(BaseModel):
    certificate_id: str
    qr_code_base64: str
    qr_code_url: str
    linkedin_share_url: str
    issued_at: datetime
    status: str

class CertificateListItem(BaseModel):
    certificate_id: str
    recipient_name: str
    course_title: str
    issued_at: datetime
    status: str

from app.models.certificate import Recipient, CertificateDetails

class IssueCertificateRequest(BaseModel):
    recipient: Recipient
    certificate: CertificateDetails
