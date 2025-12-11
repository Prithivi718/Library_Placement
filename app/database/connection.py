import sqlite3
from app.config import DB_PATH


def get_connection():
    # allow usage across threads (FastAPI background threadpool)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# Dependency for FastAPI
def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
