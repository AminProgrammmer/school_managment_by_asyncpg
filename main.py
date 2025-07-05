from fastapi import FastAPI
# from authentication import authentication
from routers import lifespan,student


app = FastAPI()
app.include_router(lifespan.router)
# app.include_router(authentication.router)
# app.include_router(admins.router)
# app.include_router(classes.router)
# app.include_router(grade.router)
# app.include_router(major.router)
# app.include_router(book.router)
app.include_router(student.router)

@app.get("/")
def Home():
    return {"hello":"hello"}