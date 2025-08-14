import asyncpg
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database.db import get_pg_conn
from authentication.authentication import authenticate_user,create_access_token,get_user
from schema import Token

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/token",response_model=Token)
async def login(form_data:OAuth2PasswordRequestForm = Depends(),
                db:asyncpg.pool.Pool = Depends(get_pg_conn)):
    user = await authenticate_user(db=db,national_code=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub":user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}
