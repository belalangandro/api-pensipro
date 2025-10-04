from sqlalchemy import text
from sqlalchemy.orm import Session

def get_member_by_id(db: Session, member_id: int):
    sql = text("SELECT id, name, status FROM members WHERE id = :id")
    return db.execute(sql, {"id": member_id}).mappings().first()

def list_members(db: Session, q: str = None, status: str = None, page: int = 1, page_size: int = 20):
    params = {}
    base = "FROM members"
    where = []
    if q:
        where.append("(name LIKE :q)")
        params["q"] = f"%{q}%"
    if status:
        where.append("status = :status")
        params["status"] = status
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    count = db.execute(text(f"SELECT COUNT(*) {base}{where_sql}"), params).scalar_one()
    offset = (page - 1) * page_size
    rows = db.execute(text(f"SELECT id, name, status {base}{where_sql} ORDER BY id DESC LIMIT :limit OFFSET :offset"),
                      {**params, "limit": page_size, "offset": offset}).mappings().all()
    return rows, count
