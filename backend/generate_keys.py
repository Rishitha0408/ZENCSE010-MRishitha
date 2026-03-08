"""
ECDSA P-256 Key Pair Generator — US-04

This module is responsible for generating a unique cryptographic key pair for the institution.
The private key is used to digitally sign certificates, while the public key is shared 
to allow anyone to verify that a certificate is authentic and has not been tampered with.

Run this ONCE before starting the application:
    python generate_keys.py
"""

# 'os' provides a way to interact with the operating system (e.g., creating folders, checking file existence).
import os
# 'sys' allows us to exit the script early if the user decides not to overwrite existing keys.
import sys
# 'cryptography' is the core library for secure cryptographic operations.
# 'ec' (Elliptic Curve) is used specifically for the ECDSA algorithm, which is modern, fast, and secure.
from cryptography.hazmat.primitives.asymmetric import ec
# 'serialization' allows us to convert the complex key objects into a format (PEM) that can be saved to a file.
from cryptography.hazmat.primitives import serialization


def generate_keys():
    """
    Main function to orchestrate the generation and storage of ECDSA P-256 keys.
    It ensures a directory exists, handles safety checks for overwriting, and performs the cryptographic generation.
    """
    keys_dir = "keys"
    
    # STEP 1: Ensure the directory for storing keys exists.
    # 'exist_ok=True' prevents an error if the folder is already there.
    os.makedirs(keys_dir, exist_ok=True)
    
    private_key_path = os.path.join(keys_dir, "private_key.pem")
    public_key_path = os.path.join(keys_dir, "public_key.pem")

    # STEP 2: Safety Check.
    # We check if a private key already exists because creating a new one will make all 
    # previously issued certificates invalid (since they were signed with the old key).
    if os.path.exists(private_key_path):
        print(f"\n[ATTENTION] The key file '{private_key_path}' already exists.")
        print("!! Overwriting this file WILL invalidate all previously signed certificates !!")
        choice = input("Are you absolutely sure you want to proceed and overwrite? (y/N): ")
        if choice.strip().lower() != 'y':
            print("Action cancelled. Existing keys were preserved.")
            sys.exit(0)

    print("\n[PROCESS] Generating a fresh ECDSA P-256 key pair...")

    # STEP 3: Generate the Private Key.
    # We use the NIST P-256 curve (also known as SECP256R1), which is widely trusted and standard.
    private_key = ec.generate_private_key(ec.SECP256R1())

    # STEP 4: Derive the Public Key.
    # The public key is mathematically linked to the private key but is safe to share publicly.
    public_key = private_key.public_key()

    # STEP 5: Serialize and Save the Private Key.
    # We convert the private key to 'PEM' format (a readable text format) and use 'PKCS8' structure.
    # For this dev setup, we use 'NoEncryption', but in production, this file should be handled with extreme care.
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(private_key_path, "wb") as f:
        f.write(private_pem)

    # STEP 6: Serialize and Save the Public Key.
    # The public key is saved in 'PEM' format using the standard 'SubjectPublicKeyInfo' structure.
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_key_path, "wb") as f:
        f.write(public_pem)

    # STEP 7: Final Confirmation.
    print(f"\n[SUCCESS] Successfully generated keys in the '{keys_dir}/' directory.")
    print(f" -> Private Key: {private_key_path}") 
    print("    *IMPORTANT: Keep this file secret and never commit it to version control (Git).")
    print(f" -> Public Key:  {public_key_path}")
    print("    *Note: This key will be used by the system to verify certificates.\n")


if __name__ == "__main__":
    # This entry point ensures the script runs when executed directly.
    generate_keys()
