# PensisPro API (FastAPI Skeleton)

Arsitektur berlapis: Api → Service → Repository → Helper (+ Schemas), dengan MySQL (raw SQL via `sqlalchemy.text`) dan JWT siap pakai.

## Quickstart
1) Buat dan edit `.env` dari `.env.example`
2) Buat venv, install dependencies:
   ```bash
   python -m venv .venv && source .venv/bin/activate  # on Windows use .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3) Jalankan dev server:
   ```bash
   uvicorn app.main:app --reload
   ```
4) Swagger UI: `http://127.0.0.1:8000/docs`

## Catatan
- Repository memakai **MySQL native query**: `from sqlalchemy import text`.
- ORM/eloquent tidak dipakai.
- Endpoint contoh `GET /api/healthz` dan `POST /api/v1/auth/login` disediakan sebagai template.
