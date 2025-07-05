from contextlib import asynccontextmanager
from sqlalchemy.orm.session import Session
from fastapi import APIRouter,FastAPI,Depends
from database.db import init_db_pool,close_db_pool,get_pg_conn
# from database.dataschema import Admins

import asyncio


# async def start_24h(db:Session):
#     while True:
#         item = db.query(Admins).where(Admins.id == 1).update({
#             "is_manager" : True
#         })
#         db.commit()
#         await asyncio.sleep(1400)




@asynccontextmanager
async def lifespan(app: FastAPI):
    # session = session_local()
    # task = asyncio.create_task(start_24h(session))
    await init_db_pool()
    yield
    await close_db_pool()




router = APIRouter(lifespan=lifespan)