import asyncpg
from fastapi import APIRouter,Depends,status,Query
from repositories import books
from database.db import get_pg_conn
from schema import BookBase,BookOutput

router = APIRouter(prefix="/books",tags=["books"])

@router.get("/{id}")
async def book_detail(id: int, db: asyncpg.Connection = Depends(get_pg_conn)) -> dict:
    book_crud = books.BookRepository(db=db)
    return await book_crud.get_record_by_id(id=id)

@router.get("")
async def list_book(
                       page : int = Query(1,ge=1),
                       page_size : int = Query(10,ge=1,le=100),
                       db : asyncpg.pool.Pool = Depends(get_pg_conn)
                       ) -> dict:
    book_crud = books.BookRepository(db=db)
    return await book_crud.get_all_records(page=page,page_size=page_size,model=BookOutput.model_fields)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_book(data: BookBase, db: asyncpg.pool.Pool = Depends(get_pg_conn)) -> dict:
    book_crud = books.BookRepository(db=db)
    return await book_crud.insert(data=data)



@router.delete("/{id}")
async def remove_book(id: int, db: asyncpg.pool.Pool = Depends(get_pg_conn)) -> dict:
    book_crud = books.BookRepository(db=db)
    return await book_crud.remove_item(id=id)

@router.put("/{id}")
async def edit_books(id: int, data: BookBase, db: asyncpg.pool.Pool = Depends(get_pg_conn)):
    book_crud = books.BookRepository(db=db)
    return await book_crud.update_record(id=id,data=data.model_dump())