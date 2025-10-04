from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/sales", tags=["Sales"])

@router.get("")
def list_stub():
    return {"message": "stub"}
