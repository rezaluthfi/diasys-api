# Prediction route

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..schemas.prediction import DiabetesInput
from ..core.ml_model import diabetes_model
from .auth import get_current_user
from datetime import datetime

router = APIRouter()


def categorize_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


@router.post("/predict")
def predict_diabetes(
    data: DiabetesInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check model availability
    if not diabetes_model.is_loaded:
        raise HTTPException(status_code=503, detail={
            "status": "error",
            "message": "ML model tidak tersedia"
        })
    
    # Calculate BMI
    bmi = data.weight / (data.height ** 2)
    
    if bmi < 10 or bmi > 70:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": f"BMI tidak valid ({bmi:.1f}). Periksa berat dan tinggi."
        })
    
    # Prepare features for prediction
    features = [
        data.pregnancies,
        data.glucose,
        data.blood_pressure,
        data.skin_thickness,
        data.insulin,
        bmi,
        data.diabetes_pedigree_function,
        data.age
    ]
    
    # Predict
    try:
        prediction, probability = diabetes_model.predict(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "message": f"Error saat prediksi: {str(e)}"
        })
    
    # Format result - convert numpy types to Python native types
    risk_level = "TINGGI" if prediction == 1 else "RENDAH"
    status = "Terindikasi Diabetes" if prediction == 1 else "Tidak Terindikasi Diabetes"
    probability_value = float(probability[1] * 100)
    
    # Generate detailed advice
    if prediction == 1:
        advice = """PERHATIAN: Hasil prediksi menunjukkan risiko tinggi diabetes. Segera lakukan tindakan berikut:

1. Konsultasikan dengan dokter untuk pemeriksaan lebih lanjut
2. Periksa kadar gula darah secara rutin
3. Kurangi konsumsi makanan tinggi gula dan karbohidrat
4. Tingkatkan aktivitas fisik minimal 30 menit per hari
5. Jaga berat badan ideal
6. Kelola stress dengan baik
7. Cukup tidur 7-8 jam per hari

PENTING: Segera hubungi tenaga medis profesional untuk diagnosis dan penanganan yang tepat."""
    else:
        advice = """BAGUS: Hasil prediksi menunjukkan risiko rendah diabetes. Namun tetap jaga kesehatan Anda dengan:

1. Menjaga pola makan sehat dan seimbang
2. Rutin berolahraga minimal 30 menit per hari
3. Cek kesehatan secara berkala
4. Hindari konsumsi gula berlebihan
5. Pertahankan berat badan ideal

Tetap lakukan medical check-up rutin minimal 1 tahun sekali."""
    
    # Get model metrics
    model_metrics = diabetes_model.get_metrics()
    
    return {
        "status": "success",
        "message": "Prediksi berhasil dilakukan",
        "data": {
            "user": {
                "name": current_user.name,
                "email": current_user.email
            },
            "prediction": {
                "risk_level": risk_level,
                "status": status,
                "probability": round(probability_value, 0),
                "probability_text": f"{probability_value:.1f}%",
                "color_indicator": "red" if prediction == 1 else "green",
                "advice": advice
            },
            "health_metrics": {
                "bmi": round(bmi, 2),
                "bmi_category": categorize_bmi(bmi),
                "glucose": data.glucose,
                "blood_pressure": data.blood_pressure,
                "age": data.age
            },
            "input_summary": {
                "weight": data.weight,
                "height": data.height,
                "insulin": data.insulin,
                "skin_thickness": data.skin_thickness,
                "diabetes_pedigree": data.diabetes_pedigree_function,
                "pregnancies": data.pregnancies
            },
            "model_info": {
                "accuracy": model_metrics["accuracy"] if model_metrics else 0,
                "model_type": model_metrics["model_type"] if model_metrics else "Machine Learning"
            },
            "disclaimer": "Hasil prediksi ini bersifat estimasi dan TIDAK menggantikan diagnosis medis profesional. Selalu konsultasikan dengan dokter untuk diagnosis dan penanganan yang tepat.",
            "timestamp": datetime.utcnow().isoformat()
        }
    }
