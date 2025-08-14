from fastapi import APIRouter,status,Depends,Query
from database.db import get_pg_conn
from repositories import personnel
from schema import PersonnelBase,PersonnelOutput
from authentication.authentication import get_current_user
import asyncpg

router = APIRouter(prefix="/Personnels",tags=["Personnels"])

@router.post("/",status_code=status.HTTP_201_CREATED)
async def add_personnel(data:PersonnelBase,
                        current_user = Depends(get_current_user),
                        db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.insert(data=data.model_dump())

@router.get("")
async def get_personnels(page : int = Query(1),
                         page_size : int = Query(10,le=100),
                         db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.get_all_records(page=page,page_size=page_size,model=PersonnelOutput.model_fields)

@router.get("/{id}")
async def get_personnel_by_id(id:int,db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.get_record_by_id(id=id)

@router.delete('/{id}')
async def remove_personnel(id:int,db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.remove_item(id=id)

@router.put("/{id}")
async def edit_personnel(id: int, data: PersonnelBase, db: asyncpg.pool.Pool = Depends(get_pg_conn)) -> PersonnelBase:
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.update_record(id=id,data=data.model_dump())
