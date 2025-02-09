from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import EmailStr

class Utilisateur(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    email:EmailStr = Field(unique=True)
    mot_de_passe:str
    nom:str
    prenom:str
    tel:str
    role:str
