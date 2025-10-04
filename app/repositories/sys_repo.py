from sqlalchemy import text
from sqlalchemy.orm import Session

def get_user_by_username(db: Session, username: str):
    sql = text("SELECT user_id, username, password_hash, full_name, email FROM sys_users WHERE username = :username")
    return db.execute(sql, {"username": username}).mappings().first()

def get_user_by_email(db: Session, email: str):
    sql = text("SELECT user_id, username, password_hash, full_name, email FROM sys_users WHERE email = :email")
    return db.execute(sql, {"email": email}).mappings().first()

def get_user_by_id(db: Session, user_id: int):
    sql = text("SELECT user_id, username, password_hash, full_name, email FROM sys_users WHERE user_id = :user_id")
    return db.execute(sql, {"user_id": user_id}).mappings().first()

def create_user(db: Session, username: str, email: str, full_name: str, password_hash: str) -> int:
    sql = text("""
        INSERT INTO sys_users (username, email, full_name, password_hash, created_at)
        VALUES (:username, :email, :full_name, :password_hash, NOW())
    """)
    res = db.execute(sql, {"username": username, "email": email, "full_name": full_name, "password_hash": password_hash})
    return res.lastrowid

def insert_session(db: Session, user_id: int, refresh_token: str, expires_at: str):
    sql = text("""
        INSERT INTO sys_user_sessions (user_id, token, expired_at)
        VALUES (:user_id, :token, :exp)
    """)
    db.execute(sql, {"user_id": user_id, "token": refresh_token, "exp": expires_at})


def get_session_by_token(db: Session, token: str):
    sql = text("""
        SELECT session_id, user_id, token, expired_at FROM sys_user_sessions WHERE token = :token
    """)
    return db.execute(sql, {"token": token}).mappings().first()

def delete_session_by_token(db: Session, token: str):
    db.execute(text("DELETE FROM sys_user_sessions WHERE token = :token"), {"token": token})

def get_roles(db: Session, user_id: int) -> list:
    sql = text("""
        SELECT r.role_name FROM sys_roles r
        JOIN sys_user_roles ur ON ur.role_id = r.role_id
        WHERE ur.user_id = :uid
    """)
    rows = db.execute(sql, {"uid": user_id}).all()
    return [r[0] for r in rows]

def get_permissions(db: Session, user_id: int) -> list:
    sql = text("""
        SELECT DISTINCT p.permission_code
        FROM sys_permissions p
        JOIN sys_role_permissions rp ON rp.permission_id = p.permission_id
        JOIN sys_user_roles ur ON ur.role_id = rp.role_id
        WHERE ur.user_id = :uid
    """)
    rows = db.execute(sql, {"uid": user_id}).all()
    return [r[0] for r in rows]
