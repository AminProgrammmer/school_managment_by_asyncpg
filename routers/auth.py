import asyncpg
import uuid
from fastapi import (APIRouter, Depends, HTTPException, status,Response,Request)
from fastapi.security import OAuth2PasswordRequestForm
from database.db import get_pg_conn
from datetime import datetime,timezone
from authentication.authentication import (authenticate_user,
                                           create_access_token,
                                           create_refresh_token,
                                           store_refresh_token,
                                           verify_refresh_token,
                                           decode_token,
                                           oauth2_scheme,
                                           revoke_refresh_token)
from jose import JWTError
from schema import Token
router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/token",response_model=Token)
async def login(response : Response,
                form_data:OAuth2PasswordRequestForm = Depends(),
                db:asyncpg.Connection = Depends(get_pg_conn)):
    user = await authenticate_user(db=db,national_code=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user["id"]),
                                             "jti": str(uuid.uuid4()),
                                             "iat": datetime.now(timezone.utc),
                                             "nbf": datetime.now(timezone.utc),
                                             "token_type" : "access"
                                             })
    refresh_token , jti , expires_at = create_refresh_token(subject=str(user["id"]))
    await store_refresh_token(db=db,id=user["id"],jti=jti,expires_at=expires_at)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/auth"

    )
    return {"access_token": access_token,"token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(response:Response,request:Request,db : asyncpg.Connection = Depends(get_pg_conn)):
    cookie_token = request.cookies.get("refresh_token")

    if not cookie_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    async with db.transaction():
        payload = await verify_refresh_token(db,cookie_token)
        user_id = payload.get("sub")
        old_jti = payload.get("jti")
        await db.execute("UPDATE refresh_tokens SET is_revoked = TRUE WHERE jti = $1", uuid.UUID(old_jti))
        new_refresh_token, new_jti, expires_at = create_refresh_token(subject=user_id)
        await store_refresh_token(db=db, id=user_id, jti=new_jti, expires_at=expires_at)

    access_token = create_access_token(data={"sub": user_id,
                                             "jti": str(uuid.uuid4()),
                                             "iat": datetime.now(timezone.utc),
                                             "nbf": datetime.now(timezone.utc),
                                             "token_type": "access"
                                             })
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/auth"
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(request: Request,response : Response, db: asyncpg.Connection = Depends(get_pg_conn)):
    cookie_token = request.cookies.get("refresh_token")
    if not cookie_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
    try:
        response.delete_cookie(key="refresh_token",path="/auth")
        payload = decode_token(cookie_token)
        jti = payload.get("jti")
        if jti is None or payload.get("token_type") != "refresh":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        await revoke_refresh_token(db=db,jti=uuid.UUID(jti))
        return {"message": "Logout successful and refresh token revoked"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
