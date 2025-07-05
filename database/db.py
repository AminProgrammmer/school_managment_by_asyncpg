import asyncpg
import asyncio
from fastapi import FastAPI

config = {
        'user':'postgres',
        'password':'Aa123456@',
        'database':'school_managment',
        'host':'localhost',
        'port': 5432
}

pool = None
# async def get_connection():
#     conn = await asyncpg.connect(**config)
#     print("connected to the database")
#     await conn.close()
#     print("connection closed....")

async def init_db_pool():
    global pool
    pool = await asyncpg.create_pool(**config)
    print("Pool Initialized...")

async def close_db_pool():
    await pool.close()
    print("❌ Pool closed")

async def get_pg_conn():
    async with pool.acquire() as conn:
        yield conn
