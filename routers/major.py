from authentication.authentication import RoleCheck

from fastapi import APIRouter,Depends
from sqlalchemy.orm.session import Session
from database.db import get_db
from database import db_major
from schema import major_Base
from authentication.authentication import RoleCheck
router = APIRouter(prefix="/Majors",tags=["major"])


@router.get("")
def majors(db:Session=Depends(get_db)):
    return db_major.get_all_major(db=db)

@router.post("")
def add_major(data_major:major_Base ,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_major.add_major(data=data_major,db=db)

@router.delete("/{id}")
def remove_major(id:int,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_major.delete_major(id=id,db=db)

@router.put("/{id}")
def edit_major(id:int,data:major_Base,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_major.edit_major(id,data,db)