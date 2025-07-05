from fastapi import APIRouter, Depends, status
from database.db import get_pg_conn
from services import level_service
from schema import Level_Base
import asyncpg
router = APIRouter(prefix="/level" tags=['level'])



@router.get("")
async def levels(db: asyncpg.Connection = Depends(get_pg_conn)):
    return await level_service.get_all_levels(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_level(data: Level_Base, db: asyncpg.Connection = Depends(get_pg_conn)):
    return await level_service.add_level(data, db)

@router.delete("/{id}")
async def remove_level(id: int, db: asyncpg.Connection = Depends(get_pg_conn)):
    return await level_service.remove_level(id, db)

@router.put("/{id}")
async def edit_level(id: int, data: Level_Base, db: asyncpg.Connection = Depends(get_pg_conn)):
    return await level_service.edit_level(id, data, db)
