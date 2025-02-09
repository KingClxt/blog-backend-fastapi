from sqlmodel import SQLModel, Field


class BlogCategorie(SQLModel, table=True):
    blog_id: int | None = Field(default=None, foreign_key="blog.id", primary_key=True)
    categorie_id: int | None = Field(default=None, foreign_key="categorie.id", primary_key=True)