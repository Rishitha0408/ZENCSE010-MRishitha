"""
API Request Schemas

This module defines 'Schemas', which act as strict protocols for what data 
a user is allowed to send to the API. Unlike 'Models' (which describe stored data), 
these focus specifically on the input received from the outside world.
"""

# 'pydantic' is used for defining and validating the structure of API requests.
from pydantic import BaseModel
# We import existing sub-components to keep our schemas consistent with our data models.
from app.models.certificate import Recipient, CertificateDetails

class IssueCertificateRequest(BaseModel):
    """
    The formal requirement for issuing a certificate.
    
    To issue a new certificate, the client must provide:
    1. recipient: The person receiving the cert (Name, Email, ID).
    2. certificate: The content of the cert (Title, Description, Skills).
    """
    recipient: Recipient
    certificate: CertificateDetails
