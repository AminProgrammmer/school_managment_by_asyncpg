from fastapi import APIRouter, status,HTTPException,Depends, Query
from database.db import get_pg_conn
from repositories import grade
from schema import GradeBase,Gradeout
from authentication.authentication import validate_teacher
import asyncpg

router = APIRouter(prefix="/grades", tags=['grades'])

@router.get("/{student_id}/grade")
async def grade_by_student_id(student_id : int,
                              is_teacher = Depends(validate_teacher),
                              db:asyncpg.Connection = Depends(get_pg_conn)):
    try:
        grade_response = await db.fetch("""
            SELECT g.id,s.name,b.name AS bookname,g.term1_continus,g.term1_final,g.term2_continus,g.term2_final,
                (
                    ((g.term1_continus * 0.4) + (g.term1_final * 0.6)) +
                    2 * ((g.term2_continus * 0.4) + (g.term2_final * 0.6))
                ) / 3 AS yearly_course,
                AVG(
                    (
                        ((g.term1_continus * 0.4) + (g.term1_final * 0.6)) +
                        2 * ((g.term2_continus * 0.4) + (g.term2_final * 0.6))
                    ) / 3
                ) OVER (PARTITION BY s.id) AS yearly_average
            FROM grade AS g
            INNER JOIN book AS b 
                ON b.id = g.course_id
            INNER JOIN students AS s 
                ON s.id = g.student_id
            WHERE g.student_id = $1;
        """,student_id)
        if not grade_response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No grades found for student_id={student_id}"
            )
        return grade_response
    except asyncpg.PostgresError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error"
        )

    except Exception as e:
        if isinstance(e,HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error"
        )


@router.get("")
async def list_grades(
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_teacher=Depends(validate_teacher),
    page: int = Query(1),
    page_size: int = Query(10, le=100),
) -> dict:
    grade_crud = grade.GradeRepository(db=db)
    return await grade_crud.get_all_records(
        page=page, page_size=page_size, model=Gradeout.model_fields
    )

@router.get("/{id}")
async def grade_detail(
    id: int,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_teacher=Depends(validate_teacher),
) -> dict:
    grade_crud = grade.GradeRepository(db=db)
    return await grade_crud.get_record_by_id(id=id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_grade(
    data: GradeBase,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_teacher=Depends(validate_teacher),
) -> dict:
    grade_crud = grade.GradeRepository(db=db)
    return await grade_crud.insert(data=data.model_dump())

@router.delete("/{id}")
async def delete_grade(
    id: int,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_teacher=Depends(validate_teacher),
) -> dict:
    grade_crud = grade.GradeRepository(db=db)
    return await grade_crud.remove_item(id=id)

@router.put("/{id}")
async def edit_grade(
    id: int,
    data: GradeBase,
    db: asyncpg.pool.Pool = Depends(get_pg_conn),
    is_teacher=Depends(validate_teacher),
) -> dict:
    grade_crud = grade.GradeRepository(db=db)
    return await grade_crud.update_record(id=id, data=data.model_dump())
