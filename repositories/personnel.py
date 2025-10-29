from . import base

class PersonnelRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"personnel")

class RelationRepository(base.BaseRepository):
    def __init__(self,db):
        super().__init__(db,"majors_of_teachers")
