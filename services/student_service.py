from fastapi import HTTPException, status
from repositories import repositories
from schema import Student_Base
import asyncpg

async def get_student_by_id(student_id: int, db:asyncpg.pool.Pool) -> dict:
    try:
        data_student = await db.fetchrow("SELECT * FROM students WHERE id = $1", student_id)
        if not data_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return dict(data_student)
    
    except asyncpg.PostgresError as e:
        raise HTTPException(detail=f"database error is : {e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        raise  HTTPException(detail=f"unexpected error is  :{e}",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def get_all_students(db:asyncpg.pool.Pool,
                           page : int = 1,
                           page_size : int = 10
                           ) -> dict:
    try:
        offset = (page-1) * page_size
        limit = page_size
        students = await repositories.get_students(db=db,limit=limit,offset=offset)
        total = await repositories.count_students(db)
        return {
            "data":students,
            "pagination" : {
                "page": page,
                "page_size" : page_size,
                "total_count" :total,
                "total_pages" : (total + page_size - 1) // page_size
            }
        }
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="Database error while fetching students")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while fetching students")

async def add_student(data : Student_Base, db : asyncpg.pool.Pool) -> dict:
    try : 
        result = await db.fetchrow(
        """
        INSERT INTO students
        (name, lastname, age, national_code, phone_number, class_id, major_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING *
        """,
        data.name,
        data.last_name,
        data.age,
        data.national_code,
        data.number,
        data.class_id,
        data.major_id,
        )
        if not result:
            raise HTTPException(status_code=400, detail="Insert failed")
        return dict(result)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(detail="duplicate entry",status_code=status.HTTP_409_CONFLICT)
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(detail="invalid forign key", status_code=status.HTTP_400_BAD_REQUEST)
    
    except asyncpg.PostgresError:
        raise  HTTPException(detail=f"error datebase ",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception:
        raise  HTTPException(detail=f"unexpected error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def remove_student(student_id: int, db:asyncpg.pool.Pool) -> dict:
    try :
        delete_query = await db.fetchrow(
            "DELETE FROM students WHERE id=$1 RETURNING *", student_id
        )
        if not delete_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found for delete")
        return {"deleted":dict(delete_query)}
    
    except asyncpg.PostgresError:
        raise  HTTPException(detail=f"error datebase",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception:
        raise  HTTPException(detail=f"unexpected error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



async def edit_student(student_id: int, data:Student_Base, db:asyncpg.pool.Pool) -> Student_Base:
    try:
        edit_query = await db.fetchrow(
            """
            UPDATE students
            SET name = $1,
                lastname = $2,
                age = $3,
                national_code = $4,
                phone_number = $5,
                class_id = $6,
                major_id = $7
            WHERE id = $8
            RETURNING *
            """,
            data.name,
            data.last_name,
            data.age,
            data.national_code,
            data.number,
            data.class_id,
            data.major_id,
            student_id,
        )
        if not edit_query:
            raise HTTPException(status_code=404, detail="Student not found to update")
        
        return Student_Base(**dict(edit_query))
    
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="Duplicate entry")
    
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(status_code=400, detail="Invalid foreign key")
    
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="Internal database error")
    
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while updating student")