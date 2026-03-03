from uuid import UUID

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import psycopg

from app.api.routes.health import router_health
from app.core.db import lifespan, get_conn
from app.schemas.documents import DocumentOut, DocumentIn
from app.services.documents import create_document, get_document

app = FastAPI(lifespan=lifespan)

app.include_router(router_health, prefix="/v1")

@app.exception_handler(psycopg.Error)
async def psycopg_error_handler(_request: Request, _exc: psycopg.Error):
    return JSONResponse(
        status_code=503,
        content={"error": {"code" : "db_unavailable", "message" : "Database unavailable"}},
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
        raise HTTPException(status_code=404, detail="Document not found")
    return res

