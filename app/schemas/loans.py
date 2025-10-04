from pydantic import BaseModel

class LoanDetail(BaseModel):
    id: int
    principal: float
