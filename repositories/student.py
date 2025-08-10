from fastapi import HTTPException, status
from . import base
from schema import StudentBase
import asyncpg

class StudentRepository(base.BaseRepository):
    def __init__(self,db):
        super().__init__(db,"students")