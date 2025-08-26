import os
import uuid
import asyncpg
from dotenv import load_dotenv
from typing import Any,Dict
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from password_hashing import Hash
from database.db import get_pg_conn
from jose import jwt,JWTError
from schema import TokenPayload
from datetime import timedelta,datetime,timezone
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 5
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_user(db:asyncpg.pool.Pool,national_code : str):
    return await db.fetchrow("select * from personnel where national_code = $1",national_code)

async def authenticate_user(db:asyncpg.pool.Pool,national_code : str,password:str):
    user = await get_user(db=db,national_code=national_code)
    if not user:
        return False
    if not await Hash.verify(plain_password=password,hashed_password=user["password"]):
        return False
    return user

async def store_refresh_token(db:asyncpg.pool.Pool,id:str,jti:str,expires_at:datetime):
    try:
        await db.execute("INSERT INTO refresh_tokens(jti,personnel_id,expires_at) VALUES($1,$2,$3)",
                                        uuid.UUID(jti),int(id),expires_at)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not store refresh token"
        )


def create_access_token(data:dict,
                        expire_delta : timedelta | None = None,
                             ):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return  encoded_jwt

def create_refresh_token(subject:str):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    jti = str(uuid.uuid4())
    to_encode = {
        "sub" : subject,
        "exp" : expire,
        "jti" : jti,
        "iat" : datetime.now(timezone.utc),
        "token_type" : "refresh"
    }
    encoded_jwt = jwt.encode(claims=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt , jti , expire

async def verify_refresh_token(db:asyncpg.pool.Pool,token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
        token_data = await db.fetchrow(
            "SELECT jti, expires_at, is_revoked FROM refresh_tokens WHERE jti = $1",
            uuid.UUID(payload["jti"])
        )
        if not token_data or token_data["is_revoked"] or token_data["expires_at"] < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="expire token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

def decode_token(token: str) -> Dict[str, Any]:
    payload = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM]
    )
    return payload

async def get_current_user(db:asyncpg.pool.Pool = Depends(get_pg_conn),
                           token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credetials",
                                          headers={"WWW-Authenticate": "Bearer"})
    expire_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Token expired",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = decode_token(token=token)
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp,tz=timezone.utc) < datetime.now(timezone.utc):
            raise expire_exception
        user_id : int = int(token_data.sub)
        if user_id is None:
            raise credentials_exception
        query = "select national_code from personnel where id = $1"
        national_code = await db.fetchrow(query,user_id)
    except JWTError as e:
        print(f"jwt:{e}")
        raise credentials_exception
    user = await get_user(db=db,national_code=str(national_code["national_code"]))
    if not user:
        raise credentials_exception
    return user

   