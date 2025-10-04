from sqlalchemy.orm import Session
from sqlalchemy import text

def notify(db: Session, member_id: int, channel: str, title: str, body: str):
    sql = text("""
    INSERT INTO notifications (member_id, channel, title, body, created_at)
    VALUES (:member_id, :channel, :title, :body, NOW())
    """)
    db.execute(sql, {"member_id": member_id, "channel": channel, "title": title, "body": body})
