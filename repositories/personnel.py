import asyncpg
from fastapi import HTTPException,status
from . import base
from schema import PersonnelBase

class PersonnelRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"personnel")