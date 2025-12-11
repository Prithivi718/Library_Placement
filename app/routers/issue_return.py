from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from app.database.connection import get_db
from app.schemas.library_schemas import IssueRequest, ReturnRequest

router = APIRouter(prefix="/api", tags=["Issue & Return"])

@router.post("/issue")
def issue_book(req: IssueRequest, db=Depends(get_db)):
    cur = db.cursor()

    # validate user
    cur.execute("SELECT * FROM users WHERE id=?", (req.user_id,))
    if not cur.fetchone():
        raise HTTPException(404, "User not found")

    # validate book
    cur.execute("SELECT * FROM books WHERE id=?", (req.book_id,))
    book = cur.fetchone()
    if not book:
        raise HTTPException(404, "Book not found")

    if book["available_copies"] <= 0:
        raise HTTPException(400, "No copies available")

    # issue
    cur.execute(
        "INSERT INTO issued_books (user_id, book_id) VALUES (?, ?)",
        (req.user_id, req.book_id)
    )
    cur.execute(
        "UPDATE books SET available_copies = available_copies - 1 WHERE id=?",
        (req.book_id,)
    )
    db.commit()

    return {"ok": True, "issue_id": cur.lastrowid}

@router.post("/return")
def return_book(req: ReturnRequest, db=Depends(get_db)):
    cur = db.cursor()

    cur.execute("SELECT * FROM issued_books WHERE id=?", (req.issue_id,))
    issue = cur.fetchone()
    if not issue:
        raise HTTPException(404, "Issue not found")

    if issue["returned"] == 1:
        raise HTTPException(400, "Already returned")

    cur.execute("""
        UPDATE issued_books
        SET returned=1, returned_at=?
        WHERE id=?
    """, (datetime.now().isoformat(), req.issue_id))

    cur.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id=?", (issue["book_id"],))

    db.commit()
    return {"ok": True}

@router.get("/issued")
def list_issued(db=Depends(get_db)):
    cur = db.cursor()

    cur.execute("""
        SELECT 
            ib.id,
            ib.user_id,
            u.name AS user_name,
            ib.book_id,
            b.title AS book_title,
            ib.issued_at,
            ib.returned,
            ib.returned_at
        FROM issued_books ib
        JOIN users u ON ib.user_id = u.id
        JOIN books b ON ib.book_id = b.id
    """)

    return {"ok": True, "issued": [dict(row) for row in cur.fetchall()]}
