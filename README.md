# DiaSys - Diabetes Prediction Backend API

API Backend untuk prediksi risiko diabetes menggunakan Machine Learning dengan autentikasi JWT, validasi lengkap, dan refresh token system.

## 🏗️ Struktur Proyek (Modular)

```
backend_diasys/
├── app/
│   ├── config.py            # Configuration dari .env
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   │   └── user.py          # User model
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py          # User validation
│   │   └── prediction.py    # Prediction validation
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication routes
│   │   └── prediction.py    # Prediction routes
│   └── core/                # Core utilities
│       ├── security.py      # Password hashing & JWT
│       └── ml_model.py      # ML model loader
│
├── main.py                  # Entry point
├── .env                     # Environment variables
├── .env.example             # Template environment
├── .gitignore               # Git ignore patterns
├── requirements.txt         # Python dependencies
├── database.db              # SQLite database
├── models/                  # ML model files
│   ├── diabetes_model.pkl
│   └── scaler.pkl
│
└── README.md                # THIS FILE
```

## ✨ Fitur

- ✅ **Autentikasi JWT** dengan access token (30 menit) & refresh token (7 hari)
- ✅ **Validasi Password**: Min 8 karakter, huruf besar/kecil, angka, karakter spesial
- ✅ **Error Handling**: Response error yang jelas per field
- ✅ **CORS**: Sudah dikonfigurasi untuk integrasi frontend
- ✅ **ML Prediction**: Prediksi risiko diabetes berdasarkan data medis
- ✅ **BMI Calculator**: Automatic BMI calculation & categorization
- ✅ **Risk Assessment**: HIGH/LOW risk dengan color indicators
- ✅ **Health Metrics**: Detailed health information dalam response
- ✅ **Modular Architecture**: Separation of concerns untuk maintainability

## 🌐 Production API

**Base URL**: `https://diasys-api.up.railway.app`

**Dokumentasi API**:

- **Swagger UI**: https://diasys-api.up.railway.app/docs
- **ReDoc**: https://diasys-api.up.railway.app/redoc

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env dan isi dengan nilai yang aman
```

**PENTING**: Ganti `SECRET_KEY` dan `REFRESH_SECRET_KEY` dengan nilai random yang kuat!

Generate key dengan:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Jalankan Server

```bash
uvicorn main:app --reload
```

Server akan berjalan di: http://localhost:8000

### 4. Akses Dokumentasi API

**Development (Local)**:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Production**:

- **Swagger UI**: https://diasys-api.up.railway.app/docs
- **ReDoc**: https://diasys-api.up.railway.app/redoc

## 📡 Endpoints

### Authentication

| Method | Endpoint    | Deskripsi                    | Auth Required |
| ------ | ----------- | ---------------------------- | ------------- |
| POST   | `/register` | Register user baru           | ❌            |
| POST   | `/login`    | Login & dapatkan tokens      | ❌            |
| POST   | `/refresh`  | Refresh access token         | ❌            |
| POST   | `/logout`   | Logout & hapus refresh token | ✅            |

### Prediction

| Method | Endpoint   | Deskripsi                | Auth Required |
| ------ | ---------- | ------------------------ | ------------- |
| POST   | `/predict` | Prediksi risiko diabetes | ✅            |

## 💡 Contoh Penggunaan

**Base URL Production**: `https://diasys-api.up.railway.app`

### Register

```bash
curl -X POST "https://diasys-api.up.railway.app/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST "https://diasys-api.up.railway.app/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePass123!"
```

Response:

```json
{
  "status": "success",
  "message": "Login berhasil",
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "user": {
      "user_id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    "expires_in": {
      "access_token": "30 minutes",
      "refresh_token": "7 days"
    }
  }
}
```

### Predict Diabetes

```bash
curl -X POST "https://diasys-api.up.railway.app/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "pregnancies": 2,
    "glucose": 120,
    "blood_pressure": 70,
    "skin_thickness": 20,
    "insulin": 80,
    "weight": 70,
    "height": 1.65,
    "diabetes_pedigree_function": 0.5,
    "age": 30
  }'
```

## 🚀 Deployment

API ini sudah di-deploy di **Railway** dengan konfigurasi:

**Platform**: Railway  
**URL**: https://diasys-api.up.railway.app  
**Python Version**: 3.13  
**Database**: SQLite (development)

**Environment Variables yang diperlukan**:

- `SECRET_KEY`
- `REFRESH_SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `API_TITLE`
- `API_DESCRIPTION`
- `API_VERSION`

## 🔐 Security Checklist

Sebelum push ke GitHub:

- ✅ File `.env` ada di `.gitignore`
- ✅ File `database.db` ada di `.gitignore`
- ✅ `SECRET_KEY` diganti dengan nilai random
- ✅ `REFRESH_SECRET_KEY` diganti dengan nilai random
- ✅ Production environment menggunakan database yang proper (PostgreSQL, MySQL)

Lihat [SECURITY_SETUP.md](SECURITY_SETUP.md) untuk panduan lengkap (jika ada).

## 🛠️ Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM untuk database
- **Pydantic** - Data validation
- **JWT** - Token-based authentication
- **Bcrypt** - Password hashing
- **Scikit-learn** - Machine Learning
- **Uvicorn** - ASGI server

## 📦 Dependencies

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.17
pydantic==2.10.2
scikit-learn==1.5.2
pydantic-settings==2.6.1
python-dotenv==1.0.1
```

## 🎯 Import Structure

Struktur modular yang jelas:

```python
# Configuration
from app.config import settings

# Models
from app.models.user import User

# Schemas
from app.schemas.user import UserRegister, UserLogin
from app.schemas.prediction import DiabetesInput

# Security utilities
from app.core.security import create_access_token, verify_password

# ML Model
from app.core.ml_model import diabetes_model

# Database
from app.database import get_db
```

## 📝 Notes

- Access token berlaku **30 menit**
- Refresh token berlaku **7 hari**
- Password harus min **8 karakter** dengan uppercase, lowercase, angka, dan karakter spesial
- BMI dihitung otomatis dari Weight (kg) dan Height (m)
- Model ML di folder `models/` (diabetes_model.pkl & scaler.pkl)

## 🤝 Kontribusi

Proyek ini adalah bagian dari Praktikum Penambangan Data Semester 5.

---
