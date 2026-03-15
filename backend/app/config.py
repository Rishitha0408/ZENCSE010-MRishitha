"""
Application Configuration Module

This module centralizes all configuration settings for the CertShield application.
By using Pydantic, we ensure that environment variables are correctly typed and 
loaded, providing a single source of truth for the entire system.
"""

# 'pydantic_settings' is an extension of Pydantic that specifically handles loading 
# configuration from environment variables (.env files) or the system environment.
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    The Settings class defines all the environment variables our application requires.
    Pydantic will automatically look for these keys in an '.env' file or the environment.
    """
    
    # The API key used for authenticating requests to the system.
    api_key: str = "default_api_key_for_dev_only"
    
    # The connection string for the MongoDB database where certificate data is stored.
    mongodb_url: str = "mongodb://localhost:27017"
    
    # File paths for the cryptographic keys used for signing and verification.
    private_key_path: str = "keys/private_key.pem"
    public_key_path: str = "keys/public_key.pem"
    
    # The base URL used when generating verification links and QR codes for certificates.
    verify_base_url: str = "http://localhost:8000/verify"

    # List of allowed origins for CORS. Used to restrict admin dashboard access.
    allowed_origins: list[str] = ["*"]

    class Config:
        """
        Configuration for the Settings class.
        Tells Pydantic to look for variables in a file named '.env'.
        """
        env_file = ".env"

# Create a singleton instance of the Settings class.
# This instance will be imported by other modules to access the configuration.
settings = Settings()
