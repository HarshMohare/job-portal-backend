from fastapi import FastAPI
from .database import engine
from . import models
from .routers import candidate , recruiter , login

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(candidate.router)
app.include_router(recruiter.router)











