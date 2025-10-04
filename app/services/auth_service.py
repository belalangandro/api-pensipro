from sqlalchemy.orm import Session
from app.repositories import sys_repo
from app.helpers.security import verify_password, create_access_token
from app.helpers.config import settings

def login(db: Session, username: str, password: str):
    user = sys_repo.get_user_by_username(db, username)
    if not user or not verify_password(password, user['password_hash']):
        return None, "Invalid credentials"
    roles = sys_repo.get_roles(db, user['id'])
    perms = sys_repo.get_permissions(db, user['id'])
    claims = {
        "preferred_username": username,
        "full_name": user['full_name'],
        "email": user['email'],
        "roles": roles,
        "permissions": perms,
    }
    token = create_access_token(str(user['id']), claims=claims, expires_in=settings.ACCESS_TOKEN_EXPIRES_SECONDS)
    return {"access_token": token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRES_SECONDS}, None
