from pydantic import BaseModel
from typing import Optional

class Member(BaseModel):
    id: int
    name: str
    status: Optional[str] = None
