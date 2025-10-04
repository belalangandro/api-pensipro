from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.get("")
def list_stub():
    return {"message": "stub"}
