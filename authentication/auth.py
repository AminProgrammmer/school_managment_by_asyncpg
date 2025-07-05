# from datetime import datetime, timedelta
# from sqlalchemy.orm.session import Session
# from jose import jwt , JWTError
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel
# from password_hashing import Hash
# #from database.db import get_db
# #from database.dataschema import Admins

# from pydantic import BaseModel

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# SECRET_KEY = "6305772ab287dcbf2e123c3c60c153284d914d21b952250eaae72d5632a57e24"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str | None = None

# # to get a string like this run:
# # openssl rand -hex 32git


# def create_access_token(data:dict,expires_delta : timedelta|None=None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES,)
#     to_encode.update({"exp":expire}) 
#     encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    
#     return encoded_jwt


# def authenticate_user(db: Session, national_code: str, password: str):
#     user = db.query(Admins).where(Admins.national_code==national_code).first()
#     if not user:
#         return False
#     elif Hash.verify(plain_password=password,hashed_password=user.password) == False:
#         return False
#     return user


# def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         national_code: str = payload.get("sub")
#         if national_code is None:
#             raise credentials_exception
#         token_data = TokenData(username=national_code)
#     except JWTError:
#         raise credentials_exception
#     user = db.query(Admins).where(Admins.national_code==national_code).first()
#     if user is None:
#         raise credentials_exception
#     return user