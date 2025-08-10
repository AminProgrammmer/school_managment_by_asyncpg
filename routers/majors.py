from fastapi import APIRouter,status,Depends,Query
from database.db import get_pg_conn
from repositories import majors
from schema import MajorBase,MajorOutput
import asyncpg

router = APIRouter(prefix="/majors",tags=["majors"])

@router.get("")
async def list_majors(db:asyncpg.pool.Pool=Depends(get_pg_conn),
                      page : int = Query(1),
                      page_size : int = Query(10,le=100)
                      ) -> dict:
    major_crud = majors.MajorsRepository(db=db)
    return await major_crud.get_all_records(page=page,page_size=page_size,model=MajorOutput.model_fields)


@router.get("/{id}")
async def major_detail(id:int,db:asyncpg.pool.Pool=Depends(get_pg_conn)) -> dict:
    major_crud = majors.MajorsRepository(db=db)
    return await major_crud.get_record_by_id(id=id)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def add_major(data:MajorBase,db:asyncpg.pool.Pool = Depends(get_pg_conn)) -> dict:
    major_crud = majors.MajorsRepository(db=db)
    return await major_crud.insert(data=data.model_dump())

@router.delete("/{id}")
async def delete_major(id:int,db:asyncpg.pool.Pool = Depends(get_pg_conn)) -> dict:
    major_crud = majors.MajorsRepository(db=db)
    return await major_crud.remove_item(id=id)


@router.put("/{id}")
async def edit_major(id:int,data:MajorBase,db:asyncpg.pool.Pool = Depends(get_pg_conn)) -> dict:
    major_crud = majors.MajorsRepository(db=db)
    return await major_crud.update_record(id=id,data=data.model_dump())