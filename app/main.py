# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse

# from app.database.init_db import init_db
# from app.routers import books, users, issue_return

# app = FastAPI(title="Library API (SQLite Version)")

# # create tables
# init_db()

# # mount routers
# app.include_router(books.router)
# app.include_router(users.router)
# app.include_router(issue_return.router)

# # serve frontend
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# @app.get("/", include_in_schema=False)
# def root():
#     return FileResponse("app/static/index.html")


from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_db import init_db
from app.routers import books, users, issue_return

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"

app = FastAPI(title="Library API (SQLite Version)")

# Allow the bundled UI (and optional dev servers like VS Code Live Server)
# to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
init_db()

# Serve the bundled frontend from a stable absolute path
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# include API routers
app.include_router(books.router)
app.include_router(users.router)
app.include_router(issue_return.router)

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(INDEX_FILE)

if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
