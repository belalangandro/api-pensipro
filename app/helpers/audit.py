from sqlalchemy.orm import Session
from sqlalchemy import text

def log_audit(db: Session, actor_id: int, action: str, ref_table: str, ref_id: int):
    sql = text("""
    INSERT INTO audit_trails (actor_id, action, reference_table, reference_id, created_at)
    VALUES (:actor_id, :action, :ref_table, :ref_id, NOW())
    """)
    db.execute(sql, {"actor_id": actor_id, "action": action, "ref_table": ref_table, "ref_id": ref_id})
