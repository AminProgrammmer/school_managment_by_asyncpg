from fastapi import APIRouter, Depends,Query,status
from database.db import get_pg_conn
from repositories import classes
from schema import ClassBase,ClassOutput
from authentication.authentication import validate_manager
import asyncpg

router = APIRouter(prefix="/classes",tags=['classes'])

@router.get("")
async def list_classes(db:asyncpg.pool.Pool=Depends(get_pg_conn),
                       is_manager=Depends(validate_manager),
                       page:int=Query(1),
                       page_size:int=Query(10,le=100)
                       ):
    class_crud =  classes.ClassRepository(db=db)
    return await class_crud.get_all_records(page=page,page_size=page_size,model=ClassOutput.model_fields)

@router.get("/{id}")
async def get_class_by_id(id : int,
                          is_manager=Depends(validate_manager),
                          db:asyncpg.pool.Pool=Depends(get_pg_conn)):
    class_crud =  classes.ClassRepository(db=db)
    return await class_crud.get_record_by_id(id=id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_class(
                    data: ClassBase,
                    is_manager=Depends(validate_manager),
                    db: asyncpg.pool.Pool = Depends(get_pg_conn)):
    class_crud = classes.ClassRepository(db=db)
    return await class_crud.insert(data=data.model_dump())

@router.delete("/{id}")
async def remove_class(
                        id: int,
                        is_manager=Depends(validate_manager),
                        db: asyncpg.pool.Pool = Depends(get_pg_conn)):
    class_crud = classes.ClassRepository(db=db)
    return await class_crud.remove_item(id=id)

@router.put("/{id}")
async def update_class(
                        id: int,
                        data: ClassBase,
                        is_manager=Depends(validate_manager),
                        db: asyncpg.pool.Pool = Depends(get_pg_conn)):
    class_crud = classes.ClassRepository(db=db)
    return await class_crud.update_record(id=id, data=data.model_dump())