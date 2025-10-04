import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "PensisPro API")
    APP_ENV: str = os.getenv("APP_ENV", "development")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/pensispro")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "changeme-super-secret")
    ACCESS_TOKEN_EXPIRES_SECONDS: int = int(os.getenv("ACCESS_TOKEN_EXPIRES_SECONDS", "1800"))
    REFRESH_TOKEN_EXPIRES_SECONDS: int = int(os.getenv("REFRESH_TOKEN_EXPIRES_SECONDS", "2592000"))

    CORS_ALLOW_ORIGINS: str = os.getenv("CORS_ALLOW_ORIGINS", "*")

settings = Settings()
