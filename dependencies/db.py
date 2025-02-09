from sqlmodel import Session
from models import models

def getSession():
    with Session(models.engine) as session:
        yield session

        