from fastapi import FastAPI
# from authentication import authentication
from lifespan import lifespan
from routers import student,level,majors,books,classes,personnel,auth


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(personnel.router)
app.include_router(student.router)
app.include_router(level.router)
app.include_router(majors.router)
app.include_router(books.router)
app.include_router(classes.router)