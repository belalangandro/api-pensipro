from sqlalchemy import text
from sqlalchemy.orm import Session

def get_user_by_username(db: Session, username: str):
    sql = text("SELECT id, username, password_hash, full_name, email FROM sys_users WHERE username = :username")
    return db.execute(sql, {"username": username}).mappings().first()

def get_roles(db: Session, user_id: int) -> list:
    sql = text("""    SELECT r.code FROM sys_roles r
    JOIN sys_user_roles ur ON ur.role_id = r.id
    WHERE ur.user_id = :uid
    """)
    rows = db.execute(sql, {"uid": user_id}).all()
    return [r[0] for r in rows]

def get_permissions(db: Session, user_id: int) -> list:
    sql = text("""    SELECT DISTINCT p.code FROM sys_permissions p
    JOIN sys_role_permissions rp ON rp.permission_id = p.id
    JOIN sys_user_roles ur ON ur.role_id = rp.role_id
    WHERE ur.user_id = :uid
    """)
    rows = db.execute(sql, {"uid": user_id}).all()
    return [r[0] for r in rows]

def insert_session(db: Session, user_id: int, refresh_token: str, expires_at: str):
    sql = text("""    INSERT INTO sys_user_sessions (user_id, token, expired_at, created_at)
    VALUES (:uid, :token, :exp, NOW())
    """)
    db.execute(sql, {"uid": user_id, "token": refresh_token, "exp": expires_at})
