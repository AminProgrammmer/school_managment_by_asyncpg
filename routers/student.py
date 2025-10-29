from fastapi import APIRouter, Depends, status,Query,HTTPException
from database.db import get_pg_conn
from schema import StudentBase,StudentOutput,ParentRelation
from repositories import student
from authentication.authentication import validate_manager
import asyncpg

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/{id}")
async def student_detail(id: int,
                         is_manager = Depends(validate_manager)
                         ,db: asyncpg.Connection = Depends(get_pg_conn)) -> dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.get_record_by_id(id=id)


@router.get("")
async def list_student(
                       page : int = Query(1,ge=1),
                       page_size : int = Query(10,ge=1,le=100),
                       is_manager = Depends(validate_manager),
                       db: asyncpg.pool.Pool = Depends(get_pg_conn)
                       ) -> dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.get_all_records(page=page,page_size=page_size,model=StudentOutput.model_fields)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_student(data: StudentBase,
                      is_manager = Depends(validate_manager),
                      db: asyncpg.pool.Pool = Depends(get_pg_conn)) -> dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.insert(data=data.model_dump())


@router.delete("/{id}")
async def remove_student(id: int,
                         is_manager = Depends(validate_manager),
                         db: asyncpg.pool.Pool = Depends(get_pg_conn)) ->dict:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.remove_item(id=id)

@router.put("/{id}")
async def edit_student(id: int,
                       data: StudentBase,
                       is_manager = Depends(validate_manager),
                       db: asyncpg.pool.Pool = Depends(get_pg_conn)) -> StudentBase:
    student_crud = student.StudentRepository(db=db)
    return await student_crud.update_record(id=id,data=data.model_dump())

@router.post("/parents")
async def add_parent(data:ParentRelation,
                     is_manager = Depends(validate_manager)
                     ,db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    parent_crud = student.RelationRepository(db=db)
    return await parent_crud.insert(data=data.model_dump())

@router.delete("/parents")
async def remove_parent(id:int,
                        is_manager = Depends(validate_manager),
                        db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    parent_crud = student.RelationRepository(db=db)
    return await parent_crud.remove_item(id=id)

@router.get("/{student_id}/parents")
async def get_parent_by_student_id(student_id:int,
                                   is_manager = Depends(validate_manager),
                                   db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    try :
        get_parents = await db.fetch("""select * from parents p inner join parents_of_students ps on p.id = ps.parent_id where ps.student_id = $1""",student_id)
        if not get_parents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found parents for student id")
        return get_parents
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409, detail="duplicate entry")

    except asyncpg.ForeignKeyViolationError:
        raise HTTPException(status_code=400, detail="invalid foreign key")

    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail="database error")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail="unexpected error")