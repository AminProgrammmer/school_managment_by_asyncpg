from fastapi import APIRouter, status, Depends, Query
from database.db import get_pg_conn
from repositories import parents
from schema import ParentBase,Parent_output
from authentication.authentication import validate_manager
import asyncpg

router = APIRouter(prefix="/parents", tags=["parents"])


@router.get("")
async def list_parents(
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_manager=Depends(validate_manager),
    page: int = Query(1),
    page_size: int = Query(10, le=100),
) -> dict:
    parents_crud = parents.ParentRepository(db=db)
    return await parents_crud.get_all_records(
        page=page, page_size=page_size, model=Parent_output.model_fields
    )


@router.get("/{id}")
async def parent_detail(
    id: int,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_manager=Depends(validate_manager),
) -> dict:
    parents_crud = parents.ParentRepository(db=db)
    return await parents_crud.get_record_by_id(id=id)



@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_parent(
    data: ParentBase,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_manager=Depends(validate_manager),
) -> dict:
    parents_crud = parents.ParentRepository(db=db)
    return await parents_crud.insert(data=data.model_dump())


@router.delete("/{id}")
async def delete_parent(
    id: int,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_manager=Depends(validate_manager),
) -> dict:
    parents_crud = parents.ParentRepository(db=db)
    return await parents_crud.remove_item(id=id)


@router.put("/{id}")
async def edit_parent(
    id: int,
    data: ParentBase,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_manager=Depends(validate_manager),
) -> dict:
    parents_crud = parents.ParentRepository(db=db)
    return await parents_crud.update_record(id=id, data=data.model_dump())
