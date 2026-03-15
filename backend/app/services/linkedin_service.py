import urllib.parse
from datetime import datetime
from app.config import settings

def generate_linkedin_share_url(cert_id: str, title: str, issued_at: datetime, institution_name: str = "CertShield Institution") -> str:
    """
    Builds a LinkedIn compatible link that pre-fills certification details.
    """
    verify_url = f"{settings.verify_base_url}/{cert_id}"
    
    linkedin_params = {
        "startTask": "CERTIFICATION_NAME",
        "name": title,
        "organizationName": institution_name,
        "issueYear": str(issued_at.year),
        "issueMonth": str(issued_at.month),
        "certUrl": verify_url,
        "certId": cert_id
    }
    
    return f"https://www.linkedin.com/profile/add?{urllib.parse.urlencode(linkedin_params)}"
