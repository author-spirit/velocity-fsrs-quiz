from fastapi import APIRouter
router = APIRouter(prefix="/quiz", tags=["quiz"])

@router.get("/")
async def get_quiz():
    return "TODO"