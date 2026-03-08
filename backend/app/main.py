"""
CertShield FastAPI Application Entry Point

This is the main brain of our server. It wires together the database, security 
middleware, rate limiting, error handling, and all the different API routes.
"""

# 'asynccontextmanager' allows us to define functions that run tasks during 
# specific parts of the app's life (like startup and shutdown).
from contextlib import asynccontextmanager
# 'FastAPI' is the modern web framework we use for building our API.
# 'Request' allows us to access information about incoming user requests.
from fastapi import FastAPI, Request
# 'CORSMiddleware' handles "Cross-Origin Resource Sharing," which allows your 
# frontend (on a different port) to securely communicate with this backend.
from fastapi.middleware.cors import CORSMiddleware
# 'slowapi' is our defense against "Spam" or "Brute Force" attacks by limiting 
# how many requests a user can make in a short time.
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
# 'RequestValidationError' is raised when a user sends data that doesn't match our models.
from fastapi.exceptions import RequestValidationError

# Import our local app modules for database logic and API routes.
from app import database
from app.routers import certificates, verification, admin
# Import custom handlers to make our error messages more "human" and helpful.
from app.exceptions.handlers import (
    CertificateNotFoundException,
    certificate_not_found_handler,
    validation_error_handler,
    generic_error_handler
)
# Internal rate limiting settings.
from app.middleware.rate_limiter import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    The Lifespan Handler: This function runs once when the app starts and once when it stops.
    It's the perfect place to open and close connections to the database.
    """
    # STARTUP: Connect to the database and prepare indexes.
    await database.create_indexes()
    print("[SYSTEM] CertShield API is now online and connected to database.")
    
    yield # The application runs while this 'yield' is active.
    
    # SHUTDOWN: Gracefully close the database connection.
    await database.close_connection()
    print("[SYSTEM] CertShield API has shut down and cleaned up resources.")

# Initialize the FastAPI application with metadata and our custom lifespan manager.
app = FastAPI(
    title="CertShield API",
    description="A secure and reliable API for issuing and verifying cryptographic certificates.",
    version="1.0.0",
    lifespan=lifespan
)

# STEP 3: Configure CORS (Cross-Origin Resource Sharing).
# During development, we allow any origin ("*") to make it easier to test from local browsers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STEP 4: Initialize the Rate Limiter.
# This attaches our security limiter to the app state so it can be used in decorators.
app.state.limiter = limiter

# STEP 5: Register Human-Friendly Exception Handlers.
# These maps translate technical Python errors into clean, standardized JSON responses for the user.
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(CertificateNotFoundException, certificate_not_found_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# STEP 6: Include Application Routers.
# This organizes our API into logical sections like "/certificates" and "/admin".
app.include_router(certificates.router, prefix="/certificates", tags=["Certificates"])
app.include_router(verification.router, prefix="/verify", tags=["Verification"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    """
    The 'Heartbeat' route: A simple endpoint to check if the API is alive.
    Rate limited to 5 requests per minute to prevent resource wastage.
    """
    return {
        "status": "online",
        "message": "Welcome to the CertShield API. Everything is running smoothly!",
        "version": "1.0.0"
    }
