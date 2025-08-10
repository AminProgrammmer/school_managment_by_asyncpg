import re
from pydantic import BaseModel,field_validator,EmailStr
from enum import Enum
from validators import (validate_national_code,
                        validate_phone_number,
                        validate_email,
                        validate_password,
                        validate_school_level)


class ParentEnum(str,Enum):
    """this is an enum. use for parent type"""
    father = "Father"
    mother = "Mother"

class ParentBase(BaseModel):
    parent_type : ParentEnum
    name : str
    lastname : str
    national_code : str
    phone_number : str
    @field_validator("national_code",mode="after")
    @classmethod
    def check_national_code(cls,value:str) -> str:
        return validate_national_code(value)
    
    @field_validator("phone_number",mode="after")
    @classmethod 
    def check_phone_number(cls,value:str) -> str:
        return validate_phone_number(value)

class PersonnelOutput(BaseModel):
    name : str
    lastname : str
    national_code : str
    phone_number : str
    email : EmailStr
    is_teacher : bool
    is_manager : bool

class PersonnelBase(BaseModel):
    """pydantic validation for personality"""
    name : str
    lastname : str
    national_code : str
    phone_number : str
    email : EmailStr
    password : str
    is_teacher : bool
    
   # and the next part we want to validate email<phonenumber<national_code<password
    @field_validator("email")
    @classmethod
    def check_email(cls, value:str) ->str:
        return validate_email(value)
    
    @field_validator("phone_number",mode="after")
    @classmethod
    def check_phone_number(cls,value:str) -> str:
        return validate_phone_number(value)
    @field_validator("national_code",mode="after")
    @classmethod
    def check_national_code(cls,value:str) -> str:
        return validate_national_code(value)
    
    @field_validator("password")
    @classmethod
    def check_password(cls,value:str)->str:
        return validate_password(value)




class StudentOutput(BaseModel):
    id : int
    name :str
    lastname :str
    age:int
    national_code :str
    phone_number:str
    class_id:int
    major_id :int



class StudentBase(BaseModel):
    """pydantic validation for student session"""
    name :str
    lastname :str
    age:int
    national_code :str
    phone_number:str
    class_id:int
    major_id :int


    @field_validator("age",mode="after")
    @classmethod
    def check_age(cls, value):
        if not 6 <= value <= 120:
            raise ValueError("Age must be between 5 and 120")
        return value

    @field_validator("class_id", "major_id",mode="after")
    @classmethod
    def check_positive_id(cls, value):
        if value <= 0:
            raise ValueError("IDs must be positive integers")
        return value
    
   #Validate Iranian national code using checksum alghorithm
    @field_validator("national_code",mode="after")
    @classmethod
    def check_national_code(cls,value:str) -> str:
        return validate_national_code(value)

    #validate phone_number
    @field_validator("phone_number",mode="after")
    @classmethod
    def check_phone_number(cls,value:str) -> str:
        return validate_phone_number(value)
        

  

class LevelBase(BaseModel):
    level : int
    @field_validator("level",mode="after")
    @classmethod
    def validate_level(cls,value):
        return validate_school_level(value=value)

class LevelOutput(BaseModel):
    id : int
    level : int    

class MajorBase(BaseModel):
    name : str
    level_id : int
    @field_validator("level_id",mode="after")
    @classmethod
    def validate_level(cls, value):
        return validate_school_level(value=value)
    
class MajorOutput(BaseModel):
    id : int
    name : str
    level_id : int
    
class BookBase(BaseModel):
    name : str
    major_id : int
class BookOutput(BaseModel):
    id : int
    name : str
    major_id : int
    
class ClassBase(BaseModel):
    name : str
    major_id : int


class ClassOutput(BaseModel):
    id:int
    name : str
    major_id : int
    
