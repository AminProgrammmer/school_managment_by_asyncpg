import asyncpg
from fastapi import HTTPException,status
from . import base
from schema import MajorBase

class MajorsRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"majors")

