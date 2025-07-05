from fastapi import APIRouter,Depends
from sqlalchemy.orm.session import Session
from database.db import get_db
from database import db_admins
from schema import Admin_Base,Admin_Detail

from authentication.authentication import RoleCheck
router = APIRouter(prefix="/admins",tags=["admin"])

@router.post("")
def add_admin(data_user:Admin_Base ,db:Session=Depends(get_db)):
    return db_admins.add_admin(data=data_user,db=db)

@router.get("/{id}")
def detail_by_id(id:int,db:Session=Depends(get_db),role=Depends(RoleCheck(True))):
    return db_admins.detail_admin(id=id,db=db)

@router.get("")
def detail_all(db:Session=Depends(get_db),role=Depends(RoleCheck(True))):
    return db_admins.get_admins(db=db)

@router.delete("/{id}")
def remove_admin(id:int,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_admins.delete_admin(id=id,db=db)