# from fastapi import APIRouter,Depends,status
# from sqlalchemy.orm.session import Session
# from fastapi.exceptions import HTTPException
# import password_hashing
# #from database.dataschema import Admins
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from authentication.auth import get_current_user,create_access_token
# from database.db import get_db

# router = APIRouter(tags=['authentication'])

# @router.post("/token")
# def login_for_access_token(form_data :OAuth2PasswordRequestForm= Depends(),db:Session=Depends(get_db)):
#     user = db.query(Admins).where(Admins.national_code==form_data.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
#     elif password_hashing.Hash.verify(plain_password=form_data.password,hashed_password=user.password) == False:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="password incorrect")
#     token = create_access_token(data={"sub":user.national_code})
#     return {"access_token": token, "token_type": "bearer"}

# class RoleCheck:
#     def __init__(self,allowed_role:bool):
#         self.allowed_method = allowed_role
        
#     def __call__(self, user = Depends(get_current_user)):
#         if user.is_manager == self.allowed_method:
#             return user
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="you dont have enough permissions")