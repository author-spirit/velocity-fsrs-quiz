from fastapi import FastAPI
from api.flashcard.routes import router as flashcard_router

app = FastAPI()

# Include all APIs by path
app.include_router(flashcard_router)

@app.get("/")
def home():
    return {"message": "velocity"}