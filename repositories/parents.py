from . import base

class ParentRepository(base.BaseRepository):
    def __init__(self,db):
        super().__init__(db,"parents")

