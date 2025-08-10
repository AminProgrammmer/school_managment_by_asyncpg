from repositories import base
class ClassRepository(base.BaseRepository):
    def __init__(self,db):
        super().__init__(db,"class")