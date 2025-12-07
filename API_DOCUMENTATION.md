# 📚 DiaSys API Documentation

## 🌐 Base URL

```
http://localhost:8000
```

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Error Handling](#error-handling)
5. [Frontend Integration Guide](#frontend-integration-guide)
6. [Security Best Practices](#security-best-practices)

---

## Overview

DiaSys adalah API prediksi risiko diabetes dengan sistem autentikasi JWT yang lengkap, termasuk refresh token untuk session management yang optimal.

### Key Features

- ✅ JWT Authentication dengan Refresh Token
- ✅ Validasi Input yang Ketat
- ✅ Response Format yang Konsisten
- ✅ Field-Level Error Messages
- ✅ Machine Learning Prediction
- ✅ BMI Calculation & Categorization
- ✅ CORS Enabled untuk Frontend Integration

### Token Expiry

- **Access Token**: 30 menit
- **Refresh Token**: 7 hari

---

## Authentication

### Token Types

#### Access Token

- Digunakan untuk mengakses protected endpoints
- Valid selama 30 menit
- Dikirim via `Authorization: Bearer {token}` header

#### Refresh Token

- Digunakan untuk mendapatkan access token baru
- Valid selama 7 hari
- Disimpan di database untuk validasi

### Authentication Flow

```
1. User Login → Dapat Access Token + Refresh Token
2. Gunakan Access Token untuk API calls
3. Access Token expired (30 menit) → Gunakan Refresh Token
4. Refresh Token → Dapat Access Token baru
5. Refresh Token expired (7 hari) → User harus login ulang
```

---

## API Endpoints

### 1. Health Check

#### `GET /`

Cek status API dan informasi endpoints.

**Response:**

```json
{
  "status": "success",
  "message": "DiaSys API is running",
  "version": "1.0.0",
  "features": {
    "authentication": "JWT with refresh token",
    "access_token_expiry": "30 minutes",
    "refresh_token_expiry": "7 days"
  },
  "endpoints": {
    "register": "/register",
    "login": "/login (returns access + refresh token)",
    "refresh": "/refresh (get new access token)",
    "logout": "/logout",
    "predict": "/predict",
    "docs": "/docs"
  }
}
```

---

### 2. Register User

#### `POST /register`

Daftarkan user baru dengan validasi ketat.

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Validasi Password:**

- ✅ Minimal 8 karakter
- ✅ Harus ada huruf besar (A-Z)
- ✅ Harus ada huruf kecil (a-z)
- ✅ Harus ada angka (0-9)
- ✅ Harus ada karakter khusus (!@#$%^&\*(),.?":{}|<>)

**Validasi Nama:**

- ✅ Minimal 2 karakter
- ✅ Hanya huruf dan spasi
- ✅ Tidak boleh hanya spasi

**Success Response (201):**

```json
{
  "status": "success",
  "message": "Registrasi berhasil",
  "data": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "next_step": "Silakan login menggunakan email dan password Anda"
  }
}
```

**Error Response (409 - Email Sudah Terdaftar):**

```json
{
  "status": "error",
  "message": "Email sudah terdaftar",
  "details": {
    "field": "email",
    "suggestion": "Silakan gunakan email lain atau login jika Anda sudah memiliki akun"
  }
}
```

**Error Response (422 - Validasi Gagal):**

```json
{
  "status": "error",
  "message": "Validasi data gagal",
  "details": {
    "errors": [
      {
        "field": "password",
        "message": "Password harus mengandung minimal satu huruf besar",
        "type": "value_error"
      },
      {
        "field": "confirm_password",
        "message": "Password dan konfirmasi password tidak cocok",
        "type": "value_error"
      }
    ]
  }
}
```

---

### 3. Login

#### `POST /login`

Login user dan dapatkan access token + refresh token.

**Request Body (Form Data):**

```
username: john@example.com  (isi dengan EMAIL, bukan username)
password: SecurePass123!
```

**cURL Example:**

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePass123!"
```

**Success Response (200):**

```json
{
  "status": "success",
  "message": "Login berhasil",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
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

**Error Response (401 - Kredensial Salah):**

```json
{
  "status": "error",
  "message": "Email atau password salah",
  "details": {
    "error_type": "invalid_credentials",
    "suggestion": "Periksa kembali email dan password Anda. Pastikan Caps Lock tidak aktif."
  }
}
```

---

### 4. Refresh Token

#### `POST /refresh`

Dapatkan access token baru menggunakan refresh token.

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200):**

```json
{
  "status": "success",
  "message": "Access token berhasil diperbarui",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "user_id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    "expires_in": "30 minutes"
  }
}
```

**Error Response (401 - Token Invalid):**

```json
{
  "status": "error",
  "message": "Refresh token tidak valid atau sudah kadaluarsa",
  "details": {
    "error_type": "invalid_refresh_token",
    "suggestion": "Silakan login kembali untuk mendapatkan token baru"
  }
}
```

---

### 5. Logout

#### `POST /logout`

Logout user dan invalidate refresh token.

**Headers:**

```
Authorization: Bearer {access_token}
```

**Success Response (200):**

```json
{
  "status": "success",
  "message": "Logout berhasil",
  "data": {
    "info": "Token telah dihapus. Silakan login kembali untuk mengakses sistem."
  }
}
```

**Error Response (401 - Unauthorized):**

```json
{
  "status": "error",
  "message": "Sesi tidak valid atau sudah kadaluarsa",
  "details": {
    "error_type": "authentication_failed"
  }
}
```

---

### 6. Predict Diabetes

#### `POST /predict`

Prediksi risiko diabetes berdasarkan data medis user.

**Headers:**

```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "glucose": 148,
  "blood_pressure": 72,
  "weight": 70.5,
  "height": 1.75,
  "age": 50,
  "insulin": 0,
  "skin_thickness": 20,
  "diabetes_pedigree_function": 0.6,
  "pregnancies": 2
}
```

**Field Descriptions & Validation:**

| Field                        | Required | Type  | Range   | Description                          |
| ---------------------------- | -------- | ----- | ------- | ------------------------------------ |
| `glucose`                    | ✅ Yes   | float | 50-400  | Kadar Glukosa Darah (mg/dL)          |
| `blood_pressure`             | ✅ Yes   | float | 40-200  | Tekanan Darah Diastolik (mm Hg)      |
| `weight`                     | ✅ Yes   | float | 20-300  | Berat Badan (kg)                     |
| `height`                     | ✅ Yes   | float | 1.0-2.5 | Tinggi Badan (meter)                 |
| `age`                        | ✅ Yes   | int   | 1-120   | Usia (tahun)                         |
| `insulin`                    | ❌ No    | float | 0-900   | Kadar Insulin (mu U/ml), default: 0  |
| `skin_thickness`             | ❌ No    | float | 0-100   | Ketebalan Kulit (mm), default: 0     |
| `diabetes_pedigree_function` | ❌ No    | float | 0-2.5   | Fungsi Silsilah Diabetes, default: 0 |
| `pregnancies`                | ❌ No    | int   | 0-20    | Jumlah Kehamilan, default: 0         |

**Success Response (200):**

```json
{
  "status": "success",
  "message": "Prediksi berhasil dilakukan",
  "data": {
    "user": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "prediction": {
      "risk_level": "TINGGI",
      "status": "Terindikasi Diabetes",
      "probability": 78.5,
      "probability_text": "78.5%",
      "color_indicator": "red",
      "advice": "⚠️ PERHATIAN: Hasil prediksi menunjukkan risiko tinggi diabetes..."
    },
    "health_metrics": {
      "bmi": 23.02,
      "bmi_category": "Normal",
      "glucose": 148,
      "blood_pressure": 72,
      "age": 50
    },
    "input_summary": {
      "weight": 70.5,
      "height": 1.75,
      "insulin": 0,
      "skin_thickness": 20,
      "diabetes_pedigree": 0.6,
      "pregnancies": 2
    },
    "model_info": {
      "accuracy": 85.06,
      "model_type": "Random Forest Classifier"
    },
    "disclaimer": "Hasil prediksi ini bersifat estimasi dan TIDAK menggantikan diagnosis medis profesional...",
    "timestamp": "2025-12-07T10:30:45.123456"
  }
}
```

**BMI Categories:**

- `< 18.5` → Underweight (Kurus)
- `18.5 - 24.9` → Normal
- `25.0 - 29.9` → Overweight (Kelebihan Berat Badan)
- `≥ 30.0` → Obese (Obesitas)

**Risk Levels:**

- `RENDAH` → color_indicator: `green`
- `TINGGI` → color_indicator: `red`

**Error Response (400 - BMI Tidak Wajar):**

```json
{
  "status": "error",
  "message": "BMI hasil perhitungan tidak wajar",
  "details": {
    "calculated_bmi": 8.5,
    "suggestion": "Periksa kembali tinggi dan berat badan Anda. BMI normal berkisar 15-40."
  }
}
```

**Error Response (401 - Unauthorized):**

```json
{
  "status": "error",
  "message": "Sesi tidak valid atau sudah kadaluarsa",
  "details": {
    "error_type": "authentication_failed"
  }
}
```

**Error Response (503 - Service Unavailable):**

```json
{
  "status": "error",
  "message": "Layanan prediksi sedang tidak tersedia",
  "details": {
    "reason": "Model machine learning belum dimuat",
    "suggestion": "Silakan coba beberapa saat lagi atau hubungi administrator"
  }
}
```

---

## Error Handling

### Standard Error Response Format

Semua error response mengikuti format konsisten:

```json
{
  "status": "error",
  "message": "Pesan error yang jelas",
  "details": {
    "error_type": "tipe_error",
    "suggestion": "Saran untuk user"
  }
}
```

### HTTP Status Codes

| Code | Meaning               | When Used                 |
| ---- | --------------------- | ------------------------- |
| 200  | OK                    | Request berhasil          |
| 201  | Created               | User berhasil didaftarkan |
| 400  | Bad Request           | Input tidak valid         |
| 401  | Unauthorized          | Token invalid/expired     |
| 409  | Conflict              | Email sudah terdaftar     |
| 422  | Unprocessable Entity  | Validasi gagal            |
| 500  | Internal Server Error | Error di server           |
| 503  | Service Unavailable   | Service tidak tersedia    |

### Validation Error Format

Untuk error validasi (422), response menyertakan detail per field:

```json
{
  "status": "error",
  "message": "Validasi data gagal",
  "details": {
    "errors": [
      {
        "field": "nama_field",
        "message": "Pesan error spesifik",
        "type": "tipe_error"
      }
    ]
  }
}
```

---

## Frontend Integration Guide

### 1. Setup Axios Interceptor (Recommended)

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor: tambahkan access token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle token expired
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Jika 401 dan belum retry
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");
        const response = await axios.post("http://localhost:8000/refresh", {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data.data;
        localStorage.setItem("access_token", access_token);

        // Retry original request dengan token baru
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh token juga expired
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

### 2. Authentication Functions

```javascript
import api from "./axios-config";

// Register
export const register = async (userData) => {
  try {
    const response = await api.post("/register", userData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

// Login
export const login = async (email, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append("username", email); // IMPORTANT: field 'username' berisi EMAIL
    formData.append("password", password);

    const response = await axios.post("http://localhost:8000/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const { access_token, refresh_token, user } = response.data.data;

    // Simpan tokens
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
    localStorage.setItem("user", JSON.stringify(user));

    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

// Logout
export const logout = async () => {
  try {
    await api.post("/logout");
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    localStorage.clear();
    window.location.href = "/login";
  }
};

// Predict Diabetes
export const predictDiabetes = async (healthData) => {
  try {
    const response = await api.post("/predict", healthData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};
```

### 3. React Example Component

```jsx
import React, { useState } from "react";
import { register } from "./api";

function RegisterForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirm_password: "",
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);

    try {
      const response = await register(formData);

      // Success
      alert(response.message);
      window.location.href = "/login";
    } catch (error) {
      if (error.details?.errors) {
        // Field-level errors
        const errorMap = {};
        error.details.errors.forEach((err) => {
          errorMap[err.field] = err.message;
        });
        setErrors(errorMap);
      } else {
        // General error
        alert(error.message || "Terjadi kesalahan");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Nama:</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div>
        <label>Email:</label>
        <input
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <label>Password:</label>
        <input
          type="password"
          value={formData.password}
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
        />
        {errors.password && <span className="error">{errors.password}</span>}
        <small>
          Min 8 karakter, harus ada huruf besar, kecil, angka, dan simbol
        </small>
      </div>

      <div>
        <label>Konfirmasi Password:</label>
        <input
          type="password"
          value={formData.confirm_password}
          onChange={(e) =>
            setFormData({ ...formData, confirm_password: e.target.value })
          }
        />
        {errors.confirm_password && (
          <span className="error">{errors.confirm_password}</span>
        )}
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Loading..." : "Daftar"}
      </button>
    </form>
  );
}

export default RegisterForm;
```

### 4. Vue.js Example

```vue
<template>
  <form @submit.prevent="handlePredict">
    <div class="form-group">
      <label>Glukosa (mg/dL):</label>
      <input
        v-model.number="formData.glucose"
        type="number"
        step="0.1"
        required
      />
      <span v-if="errors.glucose" class="error">{{ errors.glucose }}</span>
    </div>

    <div class="form-group">
      <label>Tekanan Darah (mm Hg):</label>
      <input
        v-model.number="formData.blood_pressure"
        type="number"
        step="0.1"
        required
      />
      <span v-if="errors.blood_pressure" class="error">{{
        errors.blood_pressure
      }}</span>
    </div>

    <div class="form-group">
      <label>Berat Badan (kg):</label>
      <input
        v-model.number="formData.weight"
        type="number"
        step="0.1"
        required
      />
    </div>

    <div class="form-group">
      <label>Tinggi Badan (m):</label>
      <input
        v-model.number="formData.height"
        type="number"
        step="0.01"
        required
      />
    </div>

    <div class="form-group">
      <label>Usia (tahun):</label>
      <input v-model.number="formData.age" type="number" required />
    </div>

    <button type="submit" :disabled="loading">
      {{ loading ? "Memproses..." : "Prediksi" }}
    </button>

    <!-- Result Display -->
    <div
      v-if="result"
      class="result"
      :class="result.prediction.color_indicator"
    >
      <h3>Hasil Prediksi</h3>
      <p class="risk-level">{{ result.prediction.risk_level }}</p>
      <p class="status">{{ result.prediction.status }}</p>
      <p class="probability">
        Probabilitas: {{ result.prediction.probability_text }}
      </p>
      <p class="bmi">
        BMI: {{ result.health_metrics.bmi }} ({{
          result.health_metrics.bmi_category
        }})
      </p>
      <div class="advice">{{ result.prediction.advice }}</div>
    </div>
  </form>
</template>

<script>
import { predictDiabetes } from "./api";

export default {
  data() {
    return {
      formData: {
        glucose: null,
        blood_pressure: null,
        weight: null,
        height: null,
        age: null,
        insulin: 0,
        skin_thickness: 0,
        diabetes_pedigree_function: 0,
        pregnancies: 0,
      },
      errors: {},
      loading: false,
      result: null,
    };
  },
  methods: {
    async handlePredict() {
      this.errors = {};
      this.loading = true;
      this.result = null;

      try {
        const response = await predictDiabetes(this.formData);
        this.result = response.data;
      } catch (error) {
        if (error.details?.errors) {
          error.details.errors.forEach((err) => {
            this.errors[err.field] = err.message;
          });
        } else {
          alert(error.message || "Terjadi kesalahan");
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.result.red {
  border: 2px solid #dc3545;
  background: #fff5f5;
}
.result.green {
  border: 2px solid #28a745;
  background: #f0fff4;
}
.error {
  color: #dc3545;
  font-size: 0.875rem;
}
</style>
```

### 5. Vanilla JavaScript Example

```javascript
// Login Form
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const formData = new URLSearchParams();
    formData.append("username", email); // IMPORTANT: 'username' field berisi EMAIL
    formData.append("password", password);

    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    const data = await response.json();

    if (data.status === "success") {
      localStorage.setItem("access_token", data.data.access_token);
      localStorage.setItem("refresh_token", data.data.refresh_token);
      localStorage.setItem("user", JSON.stringify(data.data.user));

      window.location.href = "/dashboard.html";
    } else {
      document.getElementById("error").textContent = data.message;
    }
  } catch (error) {
    console.error("Login error:", error);
    document.getElementById("error").textContent = "Terjadi kesalahan koneksi";
  }
});

// Predict with Auto Token Refresh
async function predictWithRetry(healthData) {
  const token = localStorage.getItem("access_token");

  let response = await fetch("http://localhost:8000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(healthData),
  });

  // Jika 401, coba refresh token
  if (response.status === 401) {
    const refreshToken = localStorage.getItem("refresh_token");
    const refreshResponse = await fetch("http://localhost:8000/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (refreshResponse.ok) {
      const refreshData = await refreshResponse.json();
      localStorage.setItem("access_token", refreshData.data.access_token);

      // Retry dengan token baru
      response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${refreshData.data.access_token}`,
        },
        body: JSON.stringify(healthData),
      });
    } else {
      // Refresh token expired, redirect ke login
      localStorage.clear();
      window.location.href = "/login.html";
      return null;
    }
  }

  return await response.json();
}
```

---

## Security Best Practices

### 1. Environment Variables

**JANGAN hardcode secret keys di production!**

Buat file `.env`:

```env
SECRET_KEY=your_super_secret_access_token_key_here
REFRESH_SECRET_KEY=your_super_secret_refresh_token_key_here
DATABASE_URL=sqlite:///./database.db
```

Update `main.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
```

### 2. CORS Configuration

Untuk production, ganti `allow_origins=["*"]` dengan domain frontend yang spesifik:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. HTTPS Only

Di production, pastikan API hanya diakses via HTTPS:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### 4. Rate Limiting

Tambahkan rate limiting untuk mencegah brute force:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/login")
@limiter.limit("5/minute")  # Max 5 login attempts per menit
def login(...):
    ...
```

### 5. Input Sanitization

Backend sudah dilengkapi validasi ketat dengan Pydantic, tapi tetap:

- ✅ Validasi di frontend juga
- ✅ Sanitize input sebelum tampilkan
- ✅ Escape HTML untuk mencegah XSS

### 6. Token Storage

**Frontend:**

- ✅ Simpan access token di `localStorage` atau `sessionStorage`
- ✅ Simpan refresh token di `httpOnly cookie` (lebih aman) atau `localStorage`
- ❌ JANGAN simpan di URL atau query params

### 7. Logout Everywhere

Untuk logout dari semua device, tambahkan:

- Token versioning di database
- Blacklist token yang sudah logout

---

## Running the API

### 1. Setup Environment

```bash
# Copy .env template
cp .env.example .env

# Edit .env dan isi SECRET_KEY & REFRESH_SECRET_KEY
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Server

```bash
uvicorn main:app --reload
```

### 4. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Testing with cURL

### Register

```bash
curl -X POST "http://localhost:8000/register" \
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
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePass123!"
```

### Predict

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "glucose": 148,
    "blood_pressure": 72,
    "weight": 70.5,
    "height": 1.75,
    "age": 50,
    "insulin": 0,
    "skin_thickness": 20,
    "diabetes_pedigree_function": 0.6,
    "pregnancies": 2
  }'
```

### Refresh Token

```bash
curl -X POST "http://localhost:8000/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN_HERE"
  }'
```

### Logout

```bash
curl -X POST "http://localhost:8000/logout" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## Support & Contact

Untuk pertanyaan atau issue, silakan hubungi tim development atau buat issue di repository.

**Happy Coding! 🚀**
