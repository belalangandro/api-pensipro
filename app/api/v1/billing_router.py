from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/billing", tags=["Billing"])

@router.get("")
def list_stub():
    return {"message": "stub"}
