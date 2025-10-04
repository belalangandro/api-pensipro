from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/lms", tags=["Lms"])

@router.get("")
def list_stub():
    return {"message": "stub"}
