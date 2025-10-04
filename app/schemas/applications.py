from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    member_id: int
    produk_id: int
    plafon_pengajuan: float
    tenor_bulan: int

class ApplicationDetail(BaseModel):
    id: int
    status: str
