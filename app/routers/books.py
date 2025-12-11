from fastapi import APIRouter, Depends, HTTPException
from app.database.connection import get_db
from app.schemas.library_schemas import BookCreate, BookUpdate

router = APIRouter(prefix="/api/books", tags=["Books"])

@router.post("")
def add_book(book: BookCreate, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute(
        "INSERT INTO books (title, author, total_copies, available_copies) VALUES (?, ?, ?, ?)",
        (book.title, book.author, book.total_copies, book.total_copies)
    )
    db.commit()
    return {"ok": True, "book_id": cur.lastrowid}

@router.get("")
def list_books(db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM books")
    return {"ok": True, "books": [dict(row) for row in cur.fetchall()]}

@router.put("/{book_id}")
def update_book(book_id: int, upd: BookUpdate, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cur.fetchone()
    if not book:
        raise HTTPException(404, "Book not found")

    new_title = upd.title if upd.title else book["title"]
    new_author = upd.author if upd.author else book["author"]

    new_total = upd.total_copies if upd.total_copies else book["total_copies"]
    diff = new_total - book["total_copies"]
    new_available = book["available_copies"] + diff

    cur.execute("""
        UPDATE books SET title=?, author=?, total_copies=?, available_copies=? WHERE id=?
    """, (new_title, new_author, new_total, new_available, book_id))

    db.commit()
    return {"ok": True}

@router.delete("/{book_id}")
def delete_book(book_id: int, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    db.commit()
    return {"ok": True}
