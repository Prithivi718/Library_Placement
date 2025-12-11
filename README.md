Mini Library (FastAPI + SQLite)
================================

Simple library tracker with a FastAPI backend and a vanilla JS frontend (served from `/`). Uses SQLite for storage, no extra services needed.

Quick start
-----------
1) Create venv & install deps  
```
python -m venv .venv
.venv\Scripts\activate  # on Windows
pip install -r requirements.txt
```

2) Run the app (from repo root)  
```
uvicorn app.main:app --reload
```

3) Open the UI  
- Preferred: http://127.0.0.1:8000/ (served by FastAPI)  
- If using another dev server (e.g., Live Server), the UI will still call the API on 8000.

API basics
----------
- `POST /api/books` `{title, author, total_copies?}` → create book  
- `GET /api/books` → list books  
- `PUT /api/books/{id}` `{title?, author?, total_copies?}` → update book  
- `DELETE /api/books/{id}` → delete book  
- `POST /api/users` `{name, email?}` → register user  
- `GET /api/users` → list users  
- `POST /api/issue` `{user_id, book_id}` → issue book  
- `POST /api/return` `{issue_id}` → return book  
- `GET /api/issued` → list issued/returned records

Notes
-----
- Database file lives at `library.db` in the project root.
- CORS is open (`*`) to let external dev servers call the API.
- Frontend assets are in `app/static/`.
