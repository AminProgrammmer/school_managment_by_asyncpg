import re

def validate_school_level(value):
    if value >=13 or value <= 0:
        raise ValueError("you can not enter level grater than 12 or lower than 1")
    return value

def validate_email(value):
    pattern  = re.compile(r"^[\w\.\-]+@(gmail|yahoo|mail|microsoft)\.(com|net)$")
    if not pattern.match(value):
        raise ValueError("please use a form of correct email.valid emails for app : (gmail,yahoo,mail,microsoft)")
    return value


def validate_password( v):
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
    


def validate_national_code(value:str) -> str:
    digits = [int(digit) for digit in value]
    pattern = re.compile(r"^\d{10}$")
    if not pattern.match(value):
        raise ValueError("your national_code is not valid")
    elif len(set(digits)) == 1:
        raise ValueError("your national_code is not valid")
    else:
        check_sum = sum(digit * (10-index) for index,digit in enumerate(digits[:9]))
        reminder = check_sum % 11
        if reminder < 2:
            if reminder != digits[9]:
                raise ValueError("your national_code is not valid")    
        else:
            if digits[9] != (11-reminder):
                raise ValueError("your national_code is not valid")
    return value

def validate_phone_number(value:str) -> str:
    pattern = re.compile(r"^09\d{9}$")
    if not pattern.match(value):
        raise ValueError("your phone number is not valid")
    return value