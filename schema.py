from pydantic import BaseModel,field_validator,EmailStr
import re

class major_Base(BaseModel):
    name:str

class Admin_Base(BaseModel):
    name : str
    last_name : str
    national_code : str
    number : str
    email : EmailStr
    password : str
    major_id : int
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value[-9:-4:] in ["gmail","yahoo"] and value[-4::] in [".net",".com"]:
            return value
        else:
            raise ValueError('email invalid')
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search("[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search("[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search("[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search("[@#$%^&+=]", v):
            raise ValueError("Password must contain at least one special character (@#$%^&+=)")
        return v
    
class Admin_Detail(BaseModel):
    id:int
    name : str
    last_name : str
    national_code : str
    number : str
    email : str
    is_manager:bool
    major_id : int


class Class_Base(BaseModel):
    name :str
    major_id :int


class book_Base(BaseModel):
    name : str
    major_id : int

class Student_Base(BaseModel):
    name :str
    last_name :str
    age:int
    national_code :str
    number:str
    class_id:int
    major_id :int
    
class Grade_base(BaseModel):
    gpa : int
    book_id : int
    student_id : int
    @field_validator("gpa")
    @classmethod
    def validate_gpa(cls,val):
        if val > 20:
            raise ValueError("you can not enter gpa grater than 20 ")
        elif val < 0 :
            raise ValueError("you can not enter gpa lower than 0 ")
        return val

class Level_Base(BaseModel):
    level : int
    @field_validator("level")
    @classmethod
    def validate_level(cls,val):
        if val >=13:
            raise ValueError("you can not enter level grater than 12 ")
        return val