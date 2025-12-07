# User schemas

from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password harus ada huruf besar')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password harus ada huruf kecil')
        if not re.search(r'\d', v):
            raise ValueError('Password harus ada angka')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password harus ada karakter spesial')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
