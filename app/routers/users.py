from fastapi import APIRouter, Depends
from app.database.connection import get_db
from app.schemas.library_schemas import UserCreate

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("")
def add_user(u: UserCreate, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (u.name, u.email))
    db.commit()
    return {"ok": True, "id": cur.lastrowid}

@router.get("")
def list_users(db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    return {"ok": True, "users": [dict(row) for row in cur.fetchall()]}
