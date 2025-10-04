from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/healthz")
def healthz():
    return {"status": "ok"}
