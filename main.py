# DiaSys API - Main Entry Point

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.database import Base, engine
from app.routes import auth, prediction

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"][1:])
        errors.append({"field": field, "message": error["msg"], "type": error["type"]})
    
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validasi data gagal",
            "details": {"errors": errors}
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"status": "error", "message": exc.detail})

# Routes
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "DiaSys API is running",
        "version": settings.API_VERSION,
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

# Include routers
app.include_router(auth.router)
app.include_router(prediction.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
