from sqlmodel import SQLModel, Field
from typing import Optional, List

class Commentaire(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    commentaire:str
    id_utiliisateur:int = Field(foreign_key='utilisateur.id')