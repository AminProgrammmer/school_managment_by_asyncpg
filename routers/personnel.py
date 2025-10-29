from fastapi import APIRouter,status,Depends,Query,HTTPException
from database.db import get_pg_conn
from repositories import personnel
from schema import PersonnelBase,PersonnelOutput,MajorRelation
from authentication.authentication import validate_manager
import asyncpg

router = APIRouter(prefix="/personnels",tags=["Personnels"])

@router.post("/",status_code=status.HTTP_201_CREATED)
async def add_personnel(data:PersonnelBase,
                        db:asyncpg.pool.Pool = Depends(get_pg_conn),
                        is_manager = Depends(validate_manager)
                        ):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.insert(data=data.model_dump())

@router.get("")
async def get_personnels(page : int = Query(1),
                         page_size : int = Query(10,le=100),
                         is_manager = Depends(validate_manager),
                         db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.get_all_records(page=page,page_size=page_size,model=PersonnelOutput.model_fields)

@router.get("/{id}")
async def get_personnel_by_id(id:int,
                              is_manager=Depends(validate_manager),
                              db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.get_record_by_id(id=id)

@router.delete('/{id}')
async def remove_personnel(id:int,
                           is_manager = Depends(validate_manager)
                           ,db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.remove_item(id=id)

@router.put("/{id}")
async def edit_personnel(id: int,
                         data : PersonnelBase,
                         is_manager=Depends(validate_manager),
                         db: asyncpg.pool.Pool = Depends(get_pg_conn),
                         ):
    personnel_crud = personnel.PersonnelRepository(db=db)
    return await personnel_crud.update_record(id=id,data=data.model_dump())

@router.post("/majors")
async def add_major(data : MajorRelation,
                    is_manager = Depends(validate_manager)
                    ,db : asyncpg.pool.Pool = Depends(get_pg_conn)):
    relation_crud = personnel.RelationRepository(db=db)
    return await relation_crud.insert(data=data.model_dump())

@router.delete("/majors/{id}")
async def remove_major(
    id: int,
    is_manager = Depends(validate_manager),
    db: asyncpg.pool.Pool = Depends(get_pg_conn)
):
    relation_crud = personnel.RelationRepository(db=db)
    return await relation_crud.remove_item(id=id)

@router.get("/parent/{teacher_id}")
async def get_major_by_teacher_id(
    teacher_id: int,
    is_manager = Depends(validate_manager),
    db: asyncpg.pool.Pool = Depends(get_pg_conn)
):
    try:
        result = await db.fetch(
            """
            SELECT m.*
            FROM majors m
            INNER JOIN majors_of_teachers mt ON m.id = mt.major_id
            WHERE mt.teacher_id = $1
            """,
            teacher_id,
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
              detail="no teachers found for this parent id",
            )
        return result

    except asyncpg.ForeignKeyViolationError:
        raise HTTPException(status_code=400, detail="invalid foreign key")

    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="database error")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail="unexpected error")

