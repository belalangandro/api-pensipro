from sqlalchemy import text
from sqlalchemy.orm import Session

def create_application(db: Session, data: dict) -> int:
    sql = text("""    INSERT INTO applications (member_id, produk_id, plafon_pengajuan, tenor_bulan, status, created_at)
    VALUES (:member_id, :produk_id, :plafon_pengajuan, :tenor_bulan, 'SUBMITTED', NOW())
    """)
    res = db.execute(sql, data)
    return res.lastrowid

def get_application(db: Session, app_id: int):
    sql = text("SELECT * FROM applications WHERE id = :id")
    return db.execute(sql, {"id": app_id}).mappings().first()
