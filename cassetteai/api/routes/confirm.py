from fastapi import APIRouter, HTTPException
from api.schemas import ConfirmRequest
from db.base import get_db

# This route handles engineer confirmation only.

router = APIRouter()


@router.post("/api/confirm")
async def confirm(request: ConfirmRequest):
    db = get_db()

    updated = db.confirm_inspection({
        "inspection_id": request.inspection_id,
        "slots": request.slots,
        "engineer": request.engineer,
        "final_status": "reviewed",
    })

    if not updated:
        raise HTTPException(status_code=404, detail="Inspection not found.")

    return {"status": "confirmed", "inspection_id": request.inspection_id}
