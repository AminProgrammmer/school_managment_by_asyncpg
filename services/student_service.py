from fastapi import HTTPException, status

async def get_student_by_id(student_id: int, db):
    data_student = await db.fetch("SELECT * FROM students WHERE id = $1", student_id)
    if not data_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return data_student

async def get_all_students(db):
    return await db.fetch("SELECT * FROM students")

async def add_student(data, db):
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

async def remove_student(student_id: int, db):
    delete_query = await db.fetchrow(
        "DELETE FROM students WHERE id=$1 RETURNING *", student_id
    )
    if not delete_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found for delete")
    return dict(delete_query)

async def edit_student(student_id: int, data, db):
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
    return dict(edit_query)
