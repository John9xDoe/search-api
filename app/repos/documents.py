# app/repos/documents.py
from datetime import datetime
from typing import Any
from uuid import UUID

def insert_document(conn, doc_id: UUID, title: str, body: str) -> dict[str, Any]:
    sql = """
    INSERT INTO documents (id, title, body)
    VALUES (%s, %s, %s)
    RETURNING id, title, body, created_at
    """
    with conn.cursor() as cur:
        cur.execute(sql, (doc_id, title, body))
        row = cur.fetchone()
    conn.commit()

    return {"id": row[0], "title": row[1], "body": row[2], "created_at": row[3]}

def get_document_by_id(conn, doc_id: UUID) -> dict[str, Any] | None:
    sql = """
    SELECT id, title, body, created_at
    FROM documents
    WHERE id = %s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (doc_id,))
        row = cur.fetchone()

    if not row:
        return None

    return {"id": row[0], "title": row[1], "body": row[2], "created_at": row[3]}
