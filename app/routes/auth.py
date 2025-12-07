# Authentication routes

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserRegister, RefreshTokenRequest
from ..core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, verify_refresh_token
)
from ..config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency untuk get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None or payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check email exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Email sudah terdaftar"
        })
    
    # Create user
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "status": "success",
        "message": "Registrasi berhasil",
        "data": {
            "user_id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "next_step": "Silakan login menggunakan email dan password Anda"
        }
    }


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Validate credentials (username adalah email)
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail={
            "status": "error",
            "message": "Email atau password salah"
        })
    
    # Create tokens
    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})
    
    # Save refresh token
    db_user.refresh_token = refresh_token
    db.commit()
    
    return {
        "status": "success",
        "message": "Login berhasil",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "user_id": db_user.id,
                "name": db_user.name,
                "email": db_user.email
            },
            "expires_in": {
                "access_token": "30 minutes",
                "refresh_token": "7 days"
            }
        }
    }


@router.post("/refresh")
def refresh_access_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    # Verify refresh token
    payload = verify_refresh_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    
    if not user or user.refresh_token != request.refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    # Create new access token
    new_access_token = create_access_token(data={"sub": email})
    
    return {
        "status": "success",
        "message": "Access token berhasil diperbarui",
        "data": {
            "access_token": new_access_token,
            "token_type": "bearer",
            "user": {
                "user_id": user.id,
                "name": user.name,
                "email": user.email
            },
            "expires_in": "30 minutes"
        }
    }


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Invalidate refresh token
    current_user.refresh_token = None
    db.commit()
    
    return {
        "status": "success",
        "message": "Logout berhasil",
        "data": {
            "info": "Token telah dihapus. Silakan login kembali untuk mengakses sistem."
        }
    }
