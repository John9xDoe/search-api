# app/services/documents.py

from uuid import uuid4, UUID

from app.schemas.documents import DocumentIn, DocumentOut
from app.repos.documents import insert_document, get_document_by_id

def create_document(conn, data: DocumentIn) -> DocumentOut:
    doc_id = uuid4()
    row = insert_document(conn, doc_id=doc_id, title=data.title, body=data.body)
    return DocumentOut(**row)

def get_document(conn, doc_id: UUID) -> DocumentOut | None:
    row = get_document_by_id(conn, doc_id)
    return DocumentOut(**row) if row else None
