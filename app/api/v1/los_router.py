from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/los", tags=["Los"])

@router.get("")
def list_stub():
    return {"message": "stub"}
