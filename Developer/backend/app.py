# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import uvicorn

# Cargar la tabla Q entrenada
model_path = "q_table_trained.npy"
q_table = np.load(model_path)

# ... (tu código de CartPoleEnv, discretize_state) ...


class State(BaseModel):
    theta: float
    theta_dot: float
    x: float
    x_dot: float
    x_ddot: float


class Prediction(BaseModel):
    action: int


app = FastAPI()


@app.post("/predict/", response_model=Prediction)
async def predict(state: State):
    try:
        state_array = np.array(
            [state.theta, state.theta_dot, state.x, state.x_dot, state.x_ddot])
        discrete_state = discretize_state(state_array, n_states)
        action = np.argmax(q_table[discrete_state])
        return {"action": action}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
