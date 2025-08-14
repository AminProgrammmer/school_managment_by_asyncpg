from passlib.context import CryptContext # type: ignore
import asyncio
pwd_cxt = CryptContext(schemes='bcrypt',deprecated = 'auto')

class Hash():
    @staticmethod
    async def generate_password_hash(password):
        return await asyncio.to_thread(pwd_cxt.hash,password)
    
    
    @staticmethod
    async def verify(hashed_password,plain_password):
        return await asyncio.to_thread(pwd_cxt.verify,plain_password,hashed_password)