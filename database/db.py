import asyncpg
from fastapi.requests import Request
from contextlib import asynccontextmanager
from typing import AsyncGenerator
class DBManager:
    def __init__(self,config:dict):
        self._config = config
        self._pool : asyncpg.pool.Pool | None = None
        
        
    async def connect(self):
        self._pool = await asyncpg.create_pool(**self._config)
        
    async def disconnect(self):
        if self._pool:
            await self._pool.close()
            
    async def acquire(self):
        if not self._pool:
            raise RuntimeError("Database  pool not initialized")
        return await self._pool.acquire()
    
    async def release(self, conn: asyncpg.Connection):
        if self._pool:
            await self._pool.release(conn)
    def get_pool(self) -> asyncpg.Pool:
        if not self._pool:
            raise RuntimeError("Pool not initialized")
        return self._pool

async def get_pg_conn(request:Request) -> AsyncGenerator[asyncpg.Connection, None]:
    conn = await request.app.state.db.acquire()
    try :
        yield conn
    finally:
        await request.app.state.db.release(conn)