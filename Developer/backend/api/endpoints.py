from fastapi import APIRouter
from api.train import train_model

router = APIRouter()

@router.post("/train/")
def train(algorithm: str):
    """
    Entrena un modelo basado en el algoritmo especificado.
    """
    result = train_model(algorithm)
    return {"message": f"Entrenamiento completado con {algorithm}", "result": result}
