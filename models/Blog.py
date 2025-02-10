from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from models.blog_category import BlogCategorie
from models.Categorie import Categorie
from pydantic import BaseModel


class Blog(SQLModel, table=True):   
    id:Optional[int] = Field(default=None, primary_key=True)
    titre:str
    published:bool = Field(default=False)
    date:str
    utilisateur_id:Optional[int] = Field(default=None, foreign_key="utilisateur.id")
    categories: Optional[List[Categorie]]= Relationship(back_populates="blogs", link_model=BlogCategorie)


class BlogRequest(BaseModel):
    titre:str
    published:bool = Field(default=False)
    date:str
    categories:List[int] 