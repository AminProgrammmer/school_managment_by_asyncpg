from authentication.authentication import RoleCheck
from fastapi import APIRouter,Depends
from sqlalchemy.orm.session import Session
from database.db import get_db
from database import db_book
from schema import book_Base
from authentication.authentication import RoleCheck
router = APIRouter(prefix="/Books",tags=["Book"])


@router.get("")
def books(db:Session=Depends(get_db)):
    return db_book.get_all_book(db=db)

@router.post("")
def add_book(data_book:book_Base ,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_book.add_book(data=data_book,db=db)

@router.delete("/{id}")
def remove_book(id:int,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_book.delete_book(id=id,db=db)

@router.put("/{id}")
def edit_book(id:int,data:book_Base,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_book.edit_book(id,data,db)