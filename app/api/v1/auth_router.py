from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, LogoutRequest, TokenPairResponse
from app.services import auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register", status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    user_id = auth_service.register(db, req.username, req.email, req.full_name or "", req.password)
    return {"id": user_id, "username": req.username, "email": req.email}

@router.post("/login", response_model=TokenPairResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, req.username, req.password)

@router.post("/refresh", response_model=TokenPairResponse)
def refresh(req: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh(db, req.refresh_token)

@router.post("/logout")
def logout(req: LogoutRequest, db: Session = Depends(get_db)):
    auth_service.logout(db, req.refresh_token)
    return {"success": True}
