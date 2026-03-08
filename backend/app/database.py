"""
Database Management Module

This module handles the connection to our MongoDB database and ensures that 
necessary indexes are created for performance and data integrity. We use Motor,
an asynchronous MongoDB driver, to keep our application non-blocking.
"""

# 'os' is used to access system environment variables if they are not specifically in settings.
import os
# 'motor.motor_asyncio' is an asynchronous MongoDB driver for Python.
# It allows us to perform database operations without blocking the execution of our FastAPI app.
from motor.motor_asyncio import AsyncIOMotorClient
# 'pymongo' is used here specifically for defining index sort directions (e.g., ASCENDING).
import pymongo
# 'app.config' provides us with the validated settings (like the database URL).
from app.config import settings

# We maintain global variables for the client and database to ensure a shared 
# connection pool throughout the application's lifecycle.
client = None
db = None

async def create_indexes():
    """
    Initializes the database connection and ensures all required indexes are present.
    Indexes significantly speed up lookups and enforce unique constraints on key fields.
    """
    global client, db
    
    # STEP 1: Connect to the Database.
    # We prefer the URL from settings, but fall back to the environment if necessary.
    mongodb_url = os.environ.get("MONGODB_URL", settings.mongodb_url)
    client = AsyncIOMotorClient(mongodb_url)
    # Connect specifically to the 'certishield' database.
    db = client.certishield
    
    print("[DATABASE] Ensuring database indexes are created...")

    # STEP 2: Configure the 'certificates' collection.
    certificates = db.certificates
    
    # 'certificate_id' must be unique and fast to look up.
    await certificates.create_index([("certificate_id", pymongo.ASCENDING)], unique=True)
    # 'data_hash' must be unique to prevent duplicate certificate contents from being issued.
    await certificates.create_index([("signature.data_hash", pymongo.ASCENDING)], unique=True)
    # We index 'recipient.email' for fast lookups of certificates by a specific student.
    await certificates.create_index([("recipient.email", pymongo.ASCENDING)])
    # We index 'status' and 'expires_at' to help with filtering active/expired certificates.
    await certificates.create_index([("status", pymongo.ASCENDING), ("expires_at", pymongo.ASCENDING)])
    
    # STEP 3: Configure the 'verification_logs' collection.
    verification_logs = db.verification_logs
    # We index 'certificate_id' to quickly see the history of a specific certificate.
    await verification_logs.create_index([("certificate_id", pymongo.ASCENDING)])
    # We index 'verified_at' for auditing and visualizing verification timestamps over time.
    await verification_logs.create_index([("verified_at", pymongo.ASCENDING)])

    print("[DATABASE] Indexes created successfully.")

async def close_connection():
    """
    Cleanly closes the database connection.
    This is called when the application is shutting down to free up system resources.
    """
    global client
    if client:
        client.close()
        print("[DATABASE] Connection pool closed.")

async def get_db():
    """
    A helper function (dependency) to retrieve the active database instance.
    This can be used in FastAPI routes to inject the database connection.
    """
    global db
    return db
