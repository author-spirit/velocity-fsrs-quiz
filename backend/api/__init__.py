from .flashcards.decks import router as decks_router
from .flashcards.reviews import router as reviews_router
from .flashcards.cards import router as cards_router
from .ui import ui_router

routers = [
    decks_router,
    reviews_router,
    cards_router,
    ui_router
]

def attach_router(app):
    for router in routers:
        app.include_router(router)