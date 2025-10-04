from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.repositories import sys_repo
from app.helpers.security import verify_password, hash_password, create_access_token, generate_refresh_token
from app.helpers.config import settings
from app.helpers.errors import UnauthorizedError, ConflictError

def _claims_for_user(db: Session, user: dict) -> dict:
    roles = sys_repo.get_roles(db, user['user_id'])
    perms = sys_repo.get_permissions(db, user['user_id'])
    return {
        "preferred_username": user['username'],
        "full_name": user.get('full_name'),
        "email": user.get('email'),
        "roles": roles,
        "permissions": perms,
    }

def register(db: Session, username: str, email: str, full_name: str, password: str) -> int:
    if sys_repo.get_user_by_username(db, username):
        raise ConflictError("Username already exists")
    if sys_repo.get_user_by_email(db, email):
        raise ConflictError("Email already exists")

    pw_hash = hash_password(password)
    user_id = sys_repo.create_user(
        db,
        username=username,
        email=email,
        full_name=full_name or "",
        password_hash=pw_hash
    )

    db.commit()
    return user_id

def login(db: Session, username: str, password: str):
    user = sys_repo.get_user_by_username(db, username)
    if not user or not verify_password(password, user['password_hash']):
        raise UnauthorizedError("Invalid credentials")
    claims = _claims_for_user(db, user)
    access_token = create_access_token(str(user['user_id']), claims=claims)
    refresh_token = generate_refresh_token()
    exp = datetime.now(timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRES_SECONDS)
    sys_repo.insert_session(
        db,
        user_id=user['user_id'],
        refresh_token=refresh_token,
        expires_at=exp.strftime("%Y-%m-%d %H:%M:%S"),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRES_SECONDS,
        "refresh_token": refresh_token,
    }

def refresh(db: Session, refresh_token: str):
    sess = sys_repo.get_session_by_token(db, refresh_token)
    if not sess:
        raise UnauthorizedError("Invalid refresh token")
    exp_dt = datetime.fromisoformat(str(sess['expired_at'])) if 'T' in str(sess['expired_at']) else datetime.strptime(str(sess['expired_at']), "%Y-%m-%d %H:%M:%S")
    if exp_dt < datetime.now():
        sys_repo.delete_session_by_token(db, refresh_token)
        raise UnauthorizedError("Refresh token expired")
    user = sys_repo.get_user_by_id(db, sess['user_id'])
    if not user:
        sys_repo.delete_session_by_token(db, refresh_token)
        raise UnauthorizedError("User not found for this session")
    claims = _claims_for_user(db, user)
    access_token = create_access_token(str(user['user_id']), claims=claims)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRES_SECONDS,
        "refresh_token": refresh_token,
    }

def logout(db: Session, refresh_token: str):
    sess = sys_repo.get_session_by_token(db, refresh_token)
    if sess:
        sys_repo.delete_session_by_token(db, refresh_token)
    return True
