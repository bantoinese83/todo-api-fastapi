# app/core/exceptions.py

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class NotFoundError(HTTPException):
    handle = HTTPException(status_code=404, detail="Resource not found")

    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, detail=message)

    @staticmethod
    async def handle_exception(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


class UnauthorizedError(HTTPException):
    handle = HTTPException(status_code=401, detail="Unauthorized")

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=401, detail=message)

    @staticmethod
    async def handle_exception(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


class BadRequestError(HTTPException):
    handle = HTTPException(status_code=400, detail="Bad request")

    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=400, detail=message)

    @staticmethod
    async def handle_exception(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


class InternalServerError(HTTPException):
    handle = HTTPException(status_code=500, detail="Internal server error")

    def __init__(self, message: str = "Internal server error"):
        super().__init__(status_code=500, detail=message)

    @staticmethod
    async def handle_exception(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
