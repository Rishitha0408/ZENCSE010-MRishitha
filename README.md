# CertiShield - Secure Digital Credential System

CertiShield is a full-stack platform for issuing, managing, and verifying tamper-proof digital certificates using ECDSA P-256 signatures and QR codes.

## 🚀 Quick Start (Docker)

To get the entire stack running in under 2 minutes:

1. **Started Docker Desktop**
2. **Clone and Run**:
   ```powershell
   docker-compose up --build
   ```
3. **Access**:
   - **Admin Dashboard**: [http://localhost:3000](http://localhost:3000)
   - **Verification Portal**: [http://localhost:3001](http://localhost:3001)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ Local Development Setup

### 1. Prerequisites
- Python 3.12+
- Node.js 18+
- MongoDB 7.0 (running locally)

### 2. Backend Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Generate Security Keys
You must generate the ECDSA key pair before running the server:
```powershell
$env:PYTHONPATH="."
python generate_keys.py
```

### 4. Configure Environment
Create `backend/.env`:
```env
API_KEY=your_secret_admin_key
MONGODB_URL=mongodb://localhost:27017
PRIVATE_KEY_PATH=keys/private_key.pem
PUBLIC_KEY_PATH=keys/public_key.pem
VERIFY_BASE_URL=http://localhost:3001/verify
```

### 5. Run the Servers
**Backend**:
```powershell
uvicorn app.main:app --reload
```

**Admin UI**:
```powershell
cd frontend-admin
npm install
npm start
```

**Verification Portal**:
```powershell
cd frontend-portal
npm install
npm start
```

---

## 🧪 Testing

Run backend unit and integration tests:
```powershell
cd backend
$env:PYTHONPATH="."
python -m unittest discover tests
```

---

## 📡 API Usage Examples

### Issue a Certificate
```bash
curl -X POST "http://localhost:8000/api/v1/certificates/" \
     -H "X-API-Key: your_secret_admin_key" \
     -H "Content-Type: application/json" \
     -d '{
       "recipient": {
         "name": "Jane Doe",
         "email": "jane@example.com",
         "student_id": "STU-001"
       },
       "certificate": {
         "title": "Master of Cyber Security",
         "description": "Excellence in cryptographic systems",
         "skills": ["Python", "ECDSA", "FastAPI"]
       }
     }'
```

### Verify a Certificate
```bash
curl -X GET "http://localhost:8000/api/v1/verify/CERT-YOUR-ID"
```

## 🔒 Security Features
- **Tamper-Evidence**: Any modification to certificate data invalidates the ECDSA signature.
- **Rate Limiting**: Public verification is limited to 60 req/min/IP.
- **Admin Auth**: Sensitive operations require a secure `X-API-Key`.
- **CORS Protection**: Admin access restricted to authorized origins.
