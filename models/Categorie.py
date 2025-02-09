from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from models.blog_category import BlogCategorie


class Categorie(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    titre:str

    blogs: Optional[List['Blog']] = Relationship(back_populates="categories", link_model=BlogCategorie)
    