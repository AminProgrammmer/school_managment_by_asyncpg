import asyncpg

async def get_students(db: asyncpg.pool.Pool,
                       limit : int,
                       offset : int):
    rows = await db.fetch("""SELECT id,name,lastname,age,national_code,class_id FROM students
                             ORDER BY id ASC
                             LIMIT $1 OFFSET $2
                             """,limit,offset)
    return [dict(row) for row in rows]

async def count_students(db:asyncpg.pool.Pool):
    row = await db.fetchrow("select count(*) from students")
    return row['count']