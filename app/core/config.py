# app/core/config.py

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://searchapi:searchapi@localhost:5432/searchapi",
)