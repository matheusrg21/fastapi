from fastapi import FastAPI
from fastapi_app import models
from fastapi_app.database import engine
from fastapi_app.routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
