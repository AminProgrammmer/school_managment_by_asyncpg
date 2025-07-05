from authentication.authentication import RoleCheck
from fastapi import APIRouter,Depends
from sqlalchemy.orm.session import Session
from database.db import get_db
from database import db_grade
from schema import Grade_base
from authentication.authentication import RoleCheck

router = APIRouter(prefix="/Grade",tags=["grade"])

@router.post("/")
def add_grade(data:Grade_base,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_grade.add_gpa_student(data=data,db=db)

@router.put("/{id}")
def edit_grade(id:int,data:Grade_base,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_grade.edit_grade(id,data,db)


@router.delete("/{id}")
def remove_grade(id:int,db:Session=Depends(get_db),role = Depends(RoleCheck(True))):
    return db_grade.delete_grade(id=id,db=db)


@router.get("/{student_id}")
def gpa_student(student_id:int,db:Session=Depends(get_db)):
    return db_grade.gpa_student(student_id,db)
