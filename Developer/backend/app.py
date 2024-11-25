from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="CartPole Reinforcement Learning API")

# Incluir las rutas definidas en endpoints
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de aprendizaje por refuerzo para CartPole"}
