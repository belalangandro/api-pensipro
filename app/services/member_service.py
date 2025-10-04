from sqlalchemy.orm import Session
from app.repositories import member_repo
from app.helpers.pagination import paginate

def get_member(member_id: int, db: Session):
    row = member_repo.get_member_by_id(db, member_id)
    return row

def list_members(db: Session, q: str = None, status: str = None, page: int = 1, page_size: int = 20):
    rows, total = member_repo.list_members(db, q=q, status=status, page=page, page_size=page_size)
    return paginate(rows, page, page_size, total)
