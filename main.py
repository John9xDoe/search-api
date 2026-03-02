import os
import uvicorn
from fastapi import FastAPI
import psycopg

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
