from fastapi import HTTPException, status
from . import base
from schema import StudentBase

class StudentRepository(base.BaseRepository):
    def __init__(self,db):
        super().__init__(db,"students")

class RelationRepository(base.BaseRepository):
    def __init__(self,db):
        super().__init__(db,"parents_of_students")
