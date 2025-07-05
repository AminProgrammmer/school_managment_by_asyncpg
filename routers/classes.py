from authentication.authentication import RoleCheck

from fastapi import APIRouter,Depends
from sqlalchemy.orm.session import Session
from database.db import get_db
from database import db_classes
from schema import Class_Base
from authentication.authentication import RoleCheck
router = APIRouter(prefix="/classes",tags=["class"])

@router.get("")
def classes(db:Session=Depends(get_db)):
    return db_classes.get_all_class(db=db)

@router.post("")
def add_class(data_class:Class_Base ,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_classes.add_class(data=data_class,db=db)

@router.delete("/{id}")
def remove_class(id:int,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_classes.delete_class(id=id,db=db)

@router.put("/{id}")
def edit_class(id:int,data:Class_Base,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_classes.edit_class(id,data,db)