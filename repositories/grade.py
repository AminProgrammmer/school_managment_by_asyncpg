from . import base

class GradeRepository(base.BaseRepository):
    def __init__(self,db):
        super().__init__(db,"grade")