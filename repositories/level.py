from repositories import base

class LevelRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"level")