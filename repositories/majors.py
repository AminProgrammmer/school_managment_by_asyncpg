from . import base

class MajorsRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"majors")

