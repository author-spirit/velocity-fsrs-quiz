from schemas.cardreviewdue import CardReviewDue
from core.logs import logger
from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from services.flashcard import Flashcard
from fastapi.templating import Jinja2Templates


ui_router = APIRouter(prefix="/ui", tags=["reviews"])
template = Jinja2Templates(directory="templates")


@ui_router.get("/due", response_class=HTMLResponse)
def due_page(request: Request):
    page = request.query_params.get("page") or 1
    decks = flashcard.get_due_decks({"page": page})
    headings = ["Deck", "Count"]
    logger.info(f"card dues {decks}")
    return template.TemplateResponse(
        "due.html", {"request": request, "title": "Card Due", "decks": decks, "headings": headings}
    )

@ui_router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return template.TemplateResponse(
        "index.html", {"request": request, "title": "Home", "app_url": "http://localhost:8000"}
    )