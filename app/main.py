from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.helpers.config import settings
from app.core.middleware import RequestIDMiddleware

from app.api.health_router import router as health_router
from app.api.v1.auth_router import router as auth_router

# Stubs
from app.api.v1.members_router import router as members_router
from app.api.v1.sales_router import router as sales_router
from app.api.v1.los_router import router as los_router
from app.api.v1.lms_router import router as lms_router
from app.api.v1.products_router import router as products_router
from app.api.v1.funder_router import router as funder_router
from app.api.v1.billing_router import router as billing_router
from app.api.v1.reports_router import router as reports_router
from app.api.v1.notifications_router import router as notifications_router

app = FastAPI(title=settings.APP_NAME)

# Middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ALLOW_ORIGINS.split(",")] if settings.CORS_ALLOW_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(members_router)
app.include_router(sales_router)
app.include_router(los_router)
app.include_router(lms_router)
app.include_router(products_router)
app.include_router(funder_router)
app.include_router(billing_router)
app.include_router(reports_router)
app.include_router(notifications_router)
