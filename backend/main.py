from fastapi import FastAPI
from api.flashcards.decks import router as decks_router
from api.flashcards.cards import router as cards_router
from api.flashcards.reviews import router as review_router

app = FastAPI()

# Setup logging middleware

# Include all APIs by path in one
for router in (review_router, decks_router, cards_router):
    app.include_router(router)

@app.get("/")
def home():
    return {"message": "velocity"}