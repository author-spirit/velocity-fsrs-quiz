from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from api.flashcards.decks import router as decks_router
from api.flashcards.cards import router as cards_router
from api.flashcards.reviews import router as review_router

app = FastAPI()

# Setup logging middleware

# Include all APIs by path in one
for router in (review_router, decks_router, cards_router):
    app.include_router(router)

template = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return JSONResponse({"message": "velocity"})

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return template.TemplateResponse("index.html", {"request": request, "title": "Home"})