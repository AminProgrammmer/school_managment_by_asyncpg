import os
import asyncpg
from dotenv import load_dotenv
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from password_hashing import Hash
from database.db import get_pg_conn
from jose import jwt,JWTError
from schema import TokenData,Token
from datetime import timedelta,datetime
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 15
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_user(db:asyncpg.pool.Pool,national_code : str):
    return await db.fetchrow("select * from personnel where national_code = $1",national_code)

def create_access_token(data:dict,
                        expire_delta : timedelta | None = None,
                             ):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return  encoded_jwt

async def authenticate_user(db:asyncpg.pool.Pool,national_code : str,password:str):
    user = await get_user(db=db,national_code=national_code)
    if not user:
        return False
    if not await Hash.verify(plain_password=password,hashed_password=user["password"]):
        return False
    return user

async def get_current_user(db:asyncpg.pool.Pool = Depends(get_pg_conn),
                           token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credetials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        national_code : str = payload.get("sub")
        if national_code is None:
            raise credentials_exception
        token_data = TokenData(national_code=national_code)
    except JWTError:
        raise credentials_exception
    user = await get_user(db=db,national_code=token_data.national_code)
    if not user:
        raise credentials_exception
    return user

