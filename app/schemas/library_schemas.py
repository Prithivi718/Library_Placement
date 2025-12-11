# app/schemas/library_schemas.py

from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    total_copies: int = 1

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    total_copies: Optional[int]

class UserCreate(BaseModel):
    name: str
    email: Optional[str]

class IssueRequest(BaseModel):
    user_id: int
    book_id: int

class ReturnRequest(BaseModel):
    issue_id: int
