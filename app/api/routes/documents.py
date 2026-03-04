from uuid import UUID

from fastapi import APIRouter

from app.core.db import get_conn
from app.core.errors import APIError
from app.schemas.documents import DocumentOut, DocumentIn
from app.services.documents import create_document, get_document

router_documents = APIRouter()

@router_documents.post("/documents", response_model=DocumentOut)
def create_document_endpoint(doc: DocumentIn):
    with get_conn() as conn:
        return create_document(conn, doc)

@router_documents.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document_endpoint(doc_id: UUID):
    with get_conn() as conn:
        res = get_document(conn, doc_id)
    if res is None:
        raise APIError(404, "not_found", "Document not found")
    return res

