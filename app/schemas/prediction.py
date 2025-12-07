# Prediction schemas

from pydantic import BaseModel, Field, validator

class DiabetesInput(BaseModel):
    pregnancies: int = Field(..., ge=0, le=20)
    glucose: float = Field(..., ge=50, le=400)
    blood_pressure: float = Field(..., ge=40, le=200)
    skin_thickness: float = Field(..., ge=0, le=100)
    insulin: float = Field(..., ge=0, le=900)
    weight: float = Field(..., ge=20, le=300, description="Berat badan (kg)")
    height: float = Field(..., ge=1.0, le=2.5, description="Tinggi badan (m)")
    diabetes_pedigree_function: float = Field(..., ge=0.0, le=2.5)
    age: int = Field(..., ge=1, le=120)
    
    @validator('height')
    def validate_height(cls, v):
        if v < 1.0 or v > 2.5:
            raise ValueError('Tinggi harus antara 1.0-2.5 meter')
        return v
