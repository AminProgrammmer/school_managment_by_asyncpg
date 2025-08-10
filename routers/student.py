from fastapi import APIRouter, Depends, status,Query
from database.db import get_pg_conn
from schema import StudentBase,StudentOutput
from repositories import student
import asyncpg

router = APIRouter(prefix="/Students", tags=["students"])

@router.get("/{id}")
async def student_detail(id: int, db: asyncpg.Connection = Depends(get_pg_conn)) -> dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.get_record_by_id(id=id)


@router.get("")
async def list_student(
                       page : int = Query(1,ge=1),
                       page_size : int = Query(10,ge=1,le=100),
                       db: asyncpg.pool.Pool = Depends(get_pg_conn)
                       ) -> dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.get_all_records(page=page,page_size=page_size,model=StudentOutput.model_fields)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_student(data: StudentBase, db: asyncpg.pool.Pool = Depends(get_pg_conn)) -> dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.insert(data=data.model_dump())


@router.delete("/{id}")
async def remove_student(id: int, db: asyncpg.pool.Pool = Depends(get_pg_conn)) ->dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.remove_item(id=id)

@router.put("/{id}")
async def edit_student(id: int, data: StudentBase, db: asyncpg.pool.Pool = Depends(get_pg_conn)) -> StudentBase:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.update_record(id=id,data=data.model_dump())
