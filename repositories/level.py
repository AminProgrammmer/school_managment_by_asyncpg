import asyncpg
from fastapi import HTTPException,status,Query
from repositories import base
from schema import LevelBase

class LevelRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"level")