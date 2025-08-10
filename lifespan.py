from contextlib import asynccontextmanager
from sqlalchemy.orm.session import Session
from fastapi import FastAPI
from database.db import DBManager
from password_hashing import Hash
import asyncpg
import asyncio

config = {
        'user':'postgres',
        'password':'Aa123456@',
        'database':'school_managment',
        'host':'localhost',
        'port': 5432
}


async def update_24_hours(conn:asyncpg.pool.Pool):
    while True:
        async with conn.acquire() as db:
            select_query = await db.fetchrow("select name from personnel limit 1")
            if not select_query:
                password = Hash.generate_password_hash(password="admin")
                add_manager = await db.execute("""INSERT INTO personnel(
                            name, lastname, national_code, phone_number, email, password, is_manager, is_teacher)
                            VALUES ('admin', 'admin', '0', '0', '0',$1, true, true)""",password)
        await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.db = DBManager(config=config)
    await app.state.db.connect()
    pool = app.state.db.get_pool()
    task = asyncio.create_task(update_24_hours(pool))
    try:
        yield
    finally:
        task.cancel()
        await app.state.db.disconnect()
    