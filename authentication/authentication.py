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
ACCESS_TOKEN_EXPIRE_TIME = int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME"))
REFRESH_TOKEN_EXPIRE_DAY = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAY"))
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
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAY)
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

async def revoke_refresh_token(db:asyncpg.Connection,jti:uuid.UUID):
    await db.execute("UPDATE refresh_tokens SET is_revoked = TRUE WHERE jti = $1",jti)


async def verify_refresh_token(db: asyncpg.Connection, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        jti = uuid.UUID(payload["jti"])
        token_data = await db.fetchrow("""
        select expires_at,is_revoked from refresh_tokens where jti = $1
        """, jti)
        if not token_data or token_data["expires_at"] < datetime.now(timezone.utc) or token_data["is_revoked"] != False:
            raise HTTPException(status_code=401, detail="Token not found or maybe expired")
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token format or signature")
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

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


async def validate_teacher(db: asyncpg.pool.Pool = Depends(get_pg_conn),
                           token: str = Depends(oauth2_scheme)):
    credential_error = HTTPException(detail="could not validate credential",
                                     status_code=status.HTTP_401_UNAUTHORIZED,
                                     headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = decode_token(token=token)
        token_data = TokenPayload(**payload)
        user_id = int(token_data.sub)
        if datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise credential_error
        query = "select is_teacher from personnel where id = $1"
        is_teacher = await db.fetchrow(query, user_id)
        if is_teacher["is_teacher"] != True:
            raise credential_error
        return is_teacher["is_teacher"]
    except JWTError as e:
        print(e)
        raise credential_error

async def validate_manager(db : asyncpg.pool.Pool = Depends(get_pg_conn),
                           token : str = Depends(oauth2_scheme)):
    
    credential_error = HTTPException(detail="could not validate credential",
                                     status_code=status.HTTP_401_UNAUTHORIZED,
                                     headers={"WWW-Authenticate" : "Bearer"})
    try :
        payload = decode_token(token=token)
        token_data = TokenPayload(**payload)
        user_id = int(token_data.sub)
        if datetime.fromtimestamp(token_data.exp,tz=timezone.utc) < datetime.now(timezone.utc):
            raise credential_error
        query = "select is_manager from personnel where id = $1"
        is_manager = await db.fetchrow(query,user_id)
        if is_manager["is_manager"] != True:
            raise credential_error
        return is_manager["is_manager"]
    except JWTError as e:
        print(e)
        raise credential_error