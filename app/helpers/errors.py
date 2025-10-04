from fastapi import Request
from fastapi.responses import JSONResponse

class DomainError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

class UnauthorizedError(DomainError):
    def __init__(self, message="Unauthorized", details=None):
        super().__init__("UNAUTHORIZED", message, 401, details)

class ForbiddenError(DomainError):
    def __init__(self, message="Forbidden", details=None):
        super().__init__("FORBIDDEN", message, 403, details)

class ConflictError(DomainError):
    def __init__(self, message="Conflict", details=None):
        super().__init__("CONFLICT", message, 409, details)

class NotFoundError(DomainError):
    def __init__(self, message="Not Found", details=None):
        super().__init__("NOT_FOUND", message, 404, details)

async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )

async def unhandled_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": "INTERNAL_ERROR", "message": "Something went wrong"},
    )
