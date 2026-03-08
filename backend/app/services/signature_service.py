"""
Digital Signature Service

This module handles the cryptographic heavy lifting for the application. 
It providing tools to "sign" certificate data (creating a unique, unforgeable seal) 
and "verify" that signature later to ensure the data hasn't been changed.
"""

# 'json' is used to convert python dictionaries into a consistent string format (canonicalization).
import json
# 'hashlib' provides the SHA-256 algorithm to create a unique 'fingerprint' of the data.
import hashlib
# 'base64' converts raw binary data (like signatures) into readable text that can be stored in a DB.
import base64
# 'cryptography' is our primary library for secure mathematical operations.
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
# 'InvalidSignature' is a specific error raised when a signature check fails.
from cryptography.exceptions import InvalidSignature
# 'app.config' tells us where our keys are located on the disk.
from app.config import settings

def _load_private_key():
    """Reads our secret private key from the disk to use for signing."""
    with open(settings.private_key_path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None # We assume the key is unencrypted for this educational setup.
        )

def sign_certificate(data: dict) -> tuple[str, str]:
    """
    Creates a unique digital signature for a certificate.
    
    How it works:
    1. It 'fingerprints' the data using SHA-256.
    2. It mathematically signs that fingerprint using the P-256 private key.
    
    Returns: (base64_encoded_signature, data_fingerprint_hex)
    """
    # CANONICALIZATION: We sort keys and remove spaces to ensure exactly the same 
    # string is generated every time, regardless of how the dictionary was built.
    canonical_data = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
    
    # HASHING: Create a 'fingerprint' of the data. Even changing one comma would change this hash.
    data_hash_hex = hashlib.sha256(canonical_data).hexdigest()
    prefixed_data_hash = f"sha256:{data_hash_hex}"
    
    # SIGNING: Use the private key to create a unique mathematical proof.
    private_key = _load_private_key()
    signature = private_key.sign(
        canonical_data,
        ec.ECDSA(hashes.SHA256())
    )
    
    # ENCODING: Convert the raw binary signature to a text string for the database.
    base64_signature = base64.b64encode(signature).decode('utf-8')
    
    return base64_signature, prefixed_data_hash

def _load_public_key():
    """Reads the non-secret public key to use for verifying certificates."""
    with open(settings.public_key_path, "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read()
        )

def verify_certificate(data: dict, signature_b64: str) -> bool:
    """
    Checks if a certificate's data is authentic.
    
    How it works:
    1. It reconstructs the expected 'canonical' data string from the certificate.
    2. It compares that data against the provided signature using the public key.
    
    Returns: True if authentic, False if tampered with or malformed.
    """
    try:
        # STEP 1: Decode the text-based signature back into raw binary.
        signature = base64.b64decode(signature_b64)
        
        # STEP 2: Re-recreate the exact same canonical string we signed originally.
        canonical_data = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
        
        # STEP 3: Load the public key (safe to use for verification).
        public_key = _load_public_key()
        
        # STEP 4: Perform the mathematical verification.
        # This will raise an InvalidSignature error if even a single byte has changed.
        public_key.verify(
            signature,
            canonical_data,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except (InvalidSignature, ValueError, TypeError, Exception) as e:
        # If anything goes wrong during verification, we treat it as an unauthenticated certificate.
        print(f"[SECURITY] Verification failed: {e}")
        return False
