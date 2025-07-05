from fastapi import APIRouter, Depends, status
from db.connection import get_pg_conn
from schema import Student_Base
from services import student_service
import asyncpg

router = APIRouter(prefix="/Students", tags=["student"])

@router.get("/{id}")
async def student_detail(id: int, db: asyncpg.Connection = Depends(get_pg_conn)):
    return await student_service.get_student_by_id(id, db)

@router.get("")
async def students(db: asyncpg.Connection = Depends(get_pg_conn)):
    return await student_service.get_all_students(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_student(data: Student_Base, db: asyncpg.Connection = Depends(get_pg_conn)):
    return await student_service.add_student(data, db)

@router.delete("/{id}")
async def remove_student(id: int, db: asyncpg.Connection = Depends(get_pg_conn)):
    return await student_service.remove_student(id, db)

@router.put("/{id}")
async def edit_student(id: int, data: Student_Base, db: asyncpg.Connection = Depends(get_pg_conn)):
    return await student_service.edit_student(id, data, db)
