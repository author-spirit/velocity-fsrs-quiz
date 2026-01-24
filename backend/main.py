from core.logs import logger
from fastapi import FastAPI
import api

app = FastAPI()

api.attach_router(app)

@app.get("/")
def root():
    return JSONResponse({"message": "velocity"})
