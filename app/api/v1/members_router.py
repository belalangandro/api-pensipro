from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/members", tags=["Members"])

@router.get("")
def list_stub():
    return {"message": "stub"}
