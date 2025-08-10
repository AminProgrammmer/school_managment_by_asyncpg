import asyncpg
from fastapi import HTTPException,status
from schema import BookBase
from repositories import base

class BookRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"book")