from fastapi import FastAPI
from app.models import models
from app.database import engine
from app.api import user,student

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(student.router)