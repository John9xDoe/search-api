# app/core/db.py

import logging
from contextlib import asynccontextmanager, contextmanager

import psycopg
from fastapi import FastAPI
from psycopg import connect

from app.core.config import DATABASE_URL


def db_ping() -> int:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            return cur.fetchone()[0]

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
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
            conn.commit()
    except psycopg.Error:
        logging.warning("Database connection failed")
        pass
    yield

@contextmanager
def get_conn():
    conn = psycopg.connect(DATABASE_URL, connect_timeout=2)
    try:
        yield conn
    finally:
        conn.close()