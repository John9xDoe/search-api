from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.documents import router_documents
from app.api.routes.health import router_health

from app.core.db import lifespan
from app.core.errors import APIError

app = FastAPI(lifespan=lifespan)

app.include_router(router_health, prefix="/v1")
app.include_router(router_documents, prefix="/v1")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Validation failed",
                "details": exc.errors(),
            }
        },
    )

@app.exception_handler(APIError)
async def api_error_handler(_request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code" : exc.code,
                "message" : exc.message
            }
        },
    )

