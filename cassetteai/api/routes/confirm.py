# POST /api/confirm
# Engineer confirms or corrects AI predictions. Writes ground truth to DB.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/confirm")
async def confirm():
    # TODO: write confirmed labels to db
    pass
