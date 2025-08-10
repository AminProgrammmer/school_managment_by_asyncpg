from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

class Hasher():
    @staticmethod
    async def generate_password_hash(password:str) -> str:
        return await pwd_context.hash(password)
    
    @staticmethod
    async def verify_password(plain_password:str, hashed_password:str) -> bool:
        return await pwd_context.verify(plain_password, hashed_password)