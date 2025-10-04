from typing import Generator
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.helpers.security import decode_access_token

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str) -> dict:
    try:
        payload = decode_access_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def require_permission(perm_code: str):
    def checker(user: dict = None):
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthenticated")
        perms = set((user.get("permissions") or []))
        if perm_code not in perms:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return True
    return checker
