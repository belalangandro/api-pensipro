import time, secrets
from typing import Dict, Any, Optional
from jose import jwt
from passlib.context import CryptContext
from app.helpers.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(subject: str, claims: Optional[Dict[str, Any]] = None, expires_in: Optional[int] = None) -> str:
    now = int(time.time())
    payload = {"sub": subject, "iat": now, "exp": now + int(expires_in or settings.ACCESS_TOKEN_EXPIRES_SECONDS)}
    if claims:
        payload.update(claims)
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)
