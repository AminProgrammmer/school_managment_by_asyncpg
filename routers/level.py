from fastapi import APIRouter, Depends, status,Query
from database.db import get_pg_conn
from repositories import level
from schema import LevelBase,LevelOutput
import asyncpg

router = APIRouter(prefix="/Levels",tags=['levels'])



@router.get("")
async def levels(db: asyncpg.pool.Pool = Depends(get_pg_conn),
                 page: int = Query(default=1,ge=1),
                 page_size : int = Query(default=10,le=100)
                 ) -> dict:
    level_crud = level.LevelRepository(db=db)
    return await level_crud.get_all_records(page=page,page_size=page_size,model=LevelOutput.model_fields)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_level(data: LevelBase, db: asyncpg.pool.Pool = Depends(get_pg_conn)):
    level_crud = level.LevelRepository(db=db)
    return await level_crud.insert(data=data)

@router.delete("/{id}")
async def remove_level(id: int, db: asyncpg.pool.Pool = Depends(get_pg_conn)):
    level_crud = level.LevelRepository(db=db)
    return await level_crud.remove_item(id=id)

