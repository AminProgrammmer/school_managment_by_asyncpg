
from repositories import base

class BookRepository(base.BaseRepository):
    def __init__(self, db):
        super().__init__(db,"book")