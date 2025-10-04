from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/funder", tags=["Funder"])

@router.get("")
def list_stub():
    return {"message": "stub"}
