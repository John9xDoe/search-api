from uuid import UUID

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import psycopg

from app.api.routes.health import router_health
from app.core.db import lifespan, get_conn
from app.core.errors import APIError
from app.schemas.documents import DocumentOut, DocumentIn
from app.services.documents import create_document, get_document

app = FastAPI(lifespan=lifespan)

app.include_router(router_health, prefix="/v1")

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

@app.post("/documents", response_model=DocumentOut)
def create_document_endpoint(doc: DocumentIn):
    with get_conn() as conn:
        return create_document(conn, doc)

@app.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document_endpoint(doc_id: UUID):
    with get_conn() as conn:
        res = get_document(conn, doc_id)
    if res is None:
        raise APIError(404, "not_found", "Document not found")
    return res

