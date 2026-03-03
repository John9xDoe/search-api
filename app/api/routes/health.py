# app/api/routes

from fastapi import APIRouter
from app.core.db import db_ping

router_health = APIRouter()

@router_health.get("/health")
def health():
    return {"db": db_ping()}