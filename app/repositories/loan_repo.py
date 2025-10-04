from sqlalchemy import text
from sqlalchemy.orm import Session

def get_loan(db: Session, loan_id: int):
    sql = text("SELECT * FROM loans WHERE id = :id")
    return db.execute(sql, {"id": loan_id}).mappings().first()
