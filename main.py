import os
from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import psycopg

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class DocumentIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = Field(min_length=10, max_length=100_000)

class DocumentOut(BaseModel):
    id: UUID
    title: str
    body: str
    created_at: datetime

app = FastAPI()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://searchapi:searchapi@localhost:5432/searchapi",
)

def db_ping() -> int:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            return cur.fetchone()[0]

@app.get("/health")
def health():
    return {"db": db_ping()}

@asynccontextmanager
async def lifespan(_app: FastAPI):
    ddl = """
    CREATE TABLE IF NOT EXISTS documents (
        id uuid PRIMARY KEY,
        title text NOT NULL,
        body text NOT NULL,
        created_at timestamptz NOT NULL DEFAULT now()
    );
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()
    yield

app = FastAPI(lifespan=lifespan)

@app.post(
    "/documents",
    response_model=DocumentOut
)
def create_document(payload: DocumentIn):
    doc_id = uuid4()
    sql = """
    INSERT INTO documents (id, title, body)
    VALUES (%s, %s, %s)
    RETURNING id, title, body, created_at
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (doc_id, payload.title, payload.body))
            row = cur.fetchone()
        conn.commit()

    return DocumentOut(id=row[0], title=row[1], body=row[2], created_at=row[3])

@app.get(
    "/documents/{doc_id}",
    response_model=DocumentOut
)
def get_document(doc_id: UUID):
    sql = """
    SELECT id, title, body, created_at
    FROM documents
    WHERE id = %s
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (doc_id,))
            row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentOut(id=row[0], title=row[1], body=row[2], created_at=row[3])