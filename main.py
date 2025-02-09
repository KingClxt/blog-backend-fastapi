from fastapi import FastAPI
from models import models
models.create_tables()

from router import categorie, auth, blog

app = FastAPI()

app.include_router(categorie.router)
app.include_router(auth.router)
app.include_router(blog.router)