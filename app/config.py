from pathlib import Path

# Resolve paths relative to the project root so the app works no matter
# where uvicorn is launched from.
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# SQLite DB lives at the project root (next to app/)
DB_PATH = PROJECT_ROOT / "library.db"
