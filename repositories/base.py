import asyncpg
from fastapi import HTTPException,status



async def pagination(db: asyncpg.pool.Pool,
                       limit : int,
                       offset : int,
                       table_name : str,
                       model : dict
                       ):
    fields = ",".join(model.keys())
    """This function selects and paginates everything from the database"""
    query = f"""SELECT {fields} FROM {table_name}
                             ORDER BY id ASC
                             LIMIT $1 OFFSET $2
                             """
    rows = await db.fetch(query,limit,offset)
    return [dict(row) for row in rows]


async def count_object(db:asyncpg.pool.Pool,table_name:str):
    """This function is counting the all of the items in database table"""
    row = await db.fetchrow(f"select count(*) from {table_name}")
    return row['count']

async def paginated_response_model(db:asyncpg.pool.Pool,
                                   table_name:str,page:int,
                                   page_size:int,
                                   model:dict) -> dict:
    try:
        limit = page_size
        offset = (page-1) * page_size
        paginate = await pagination(db=db,limit=limit,offset=offset,table_name=table_name,model=model)
        total_item = await count_object(db=db,table_name=table_name)
        return {"data":paginate,
                "pagination":{
                    "page":page,
                    "page_size":page_size,
                    "total_item":total_item,
                    "total_pages":(total_item + page_size - 1) // page_size

                }}
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="Database error while fetching ....")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error while fetching ....")

    
class BaseRepository:
    """In this section
    we will write a dynamic crud operation
    to avoid duplicate coding"""
    def  __init__(self,db:asyncpg.pool.Pool,table_name:str):
        self.db = db
        self.table_name = table_name
        
    async def update_record(self,id:int,data:dict):
        if not data:
            raise HTTPException(status_code=400, detail="no data to update")
        try:
            keys = list(data.keys())
            values = list(data.values())
            placeholders =",".join(f"{key} = ${i+1}" for i , key in enumerate(keys))
            values.append(id)
            where_placeholder = f"${len(values)}"
            query = f"""
            UPDATE {self.table_name}
            SET {placeholders}
            WHERE id = {where_placeholder}
            RETURNING *
            """
            updating_row = await self.db.fetchrow(query,*values)
            if not updating_row:
                raise HTTPException(status_code=404, detail="item not found for update")
            return dict(updating_row)

        except asyncpg.UniqueViolationError:
            raise HTTPException(status_code=409, detail="duplicate entry")

        except asyncpg.ForeignKeyViolationError:
            raise HTTPException(status_code=400, detail="invalid foreign key")

        except asyncpg.PostgresError as e:
            print(e)
            raise HTTPException(status_code=500, detail="database error")

        except Exception as e:
            print(e)
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail="unexpected error")
        
        
    async def get_record_by_id(self,id:int) ->  dict:
        try:
            record = await self.db.fetchrow(f"select * from {self.table_name} where id = $1",id)
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found record")
            return dict(record)
        except asyncpg.PostgresError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="database error")
        except Exception as e:
            if isinstance(e,HTTPException):
                raise e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="unexpected error")
    
        
    async def get_all_records(self,page:int,page_size:int,model:dict) -> dict:
        try:
            records = await paginated_response_model(db=self.db,
                                                     table_name=self.table_name,
                                                     page=page,
                                                     page_size=page_size,
                                                     model=model)
            if not records:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found record")
            return records
        except asyncpg.PostgresError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="database error")
        except Exception as e:
            if isinstance(e,HTTPException):
                raise e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="unexpected error")
    
    async def insert(self,data:dict) -> dict:
        keys = data.keys()
        values = list(data.values())
        columns = ",".join(keys)
        placeholders = ",".join(f"${i+1}" for i in range(len(values)))
        query = f"INSERT INTO {self.table_name}({columns}) VALUES({placeholders}) RETURNING *"
        try:
            add_query = await self.db.fetchrow(query,*values)
            if not add_query:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="insert field")
            return dict(add_query)
        except asyncpg.UniqueViolationError:
            raise HTTPException(detail="duplicate entry",status_code=status.HTTP_409_CONFLICT)
    
        except asyncpg.ForeignKeyViolationError:
            raise HTTPException(detail="invalid forign key", status_code=status.HTTP_400_BAD_REQUEST)
    
        except asyncpg.PostgresError as e:
            print(e)
            raise  HTTPException(detail=f"error datebase ",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        except Exception as e:
            if isinstance(e,HTTPException):
                raise e
            raise  HTTPException(detail=f"unexpected error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def remove_item(self,id:int) -> dict:
        try:
            remove_query = await self.db.fetchrow(f"DELETE FROM {self.table_name} WHERE ID = $1 RETURNING *",id)
            if not remove_query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found item for delete")
            return dict(remove_query)
        except asyncpg.ForeignKeyViolationError:
            raise  HTTPException(detail=f"invalid foreign key",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except asyncpg.PostgresError as e:
            raise  HTTPException(detail=f"error datebase ",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            if isinstance(e,HTTPException):
                raise e
            raise HTTPException(detail=f"unexpected error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
