from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])

@router.get("")
def list_stub():
    return {"message": "stub"}
