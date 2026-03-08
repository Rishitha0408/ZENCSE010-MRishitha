# CertiShield

CertiShield is a secure certification and verification platform using digital signatures (ECDSA P-256) and QR codes.

## Tech Stack
- **Backend**: FastAPI (Python 3.12), MongoDB 7.0 (Motor async), Pydantic v2, cryptography, qrcode[pil], slowapi
- **Admin UI**: React 18
- **Verification Portal**: React 18
- **Deployment**: Docker & Docker Compose

## Structure
- `backend/`: FastAPI application handling digital signatures, DB interactions, and QR code generation.
- `admin-ui/`: React UI for administrators to generate and manage certificates.
- `verification-portal/`: Public-facing React application to scan/verify document QR codes.
- `docker-compose.yml`: Local orchestraion.

## Setup
Run the following to start all services locally:
```bash
docker-compose up --build
```
