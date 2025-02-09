from sqlmodel import create_engine, SQLModel
from models import Blog, blog_category, Categorie, Commentaire, Utilisateur

engine = create_engine("postgresql://postgres:admin@localhost:5432/Blog_DB")

def create_tables():
    SQLModel.metadata.create_all(engine)

