from fastapi import Depends, APIRouter, HTTPException
from dependencies.auth import user_dependency
from dependencies.db import getSession
from models.Blog import Blog, BlogRequest
from sqlmodel import select, Session
from starlette import status
from models.Categorie import Categorie
from typing import Optional

router = APIRouter(
    prefix="/blogs",
    tags=["BLOG"]
)



# Récuperation des articles de blog
@router.get('/', status_code=status.HTTP_200_OK)
async def getAllBlogs(search:Optional[str] = None, categorie:Optional[str] = None, db: Session = Depends(getSession)):
    blogs = db.exec(select(Blog)).all()
    
    # Accompagner le blog de sa categorie
    blogs_filter = [
        {
            "blog":blog,
            "categories":[categorie_item.titre.lower() for categorie_item in blog.categories]
        }
        for blog in blogs
    ]
    
    # Effectuer un filtre si jamais il y en a
    if search:
        blogs_filter = [blog for blog in blogs_filter if search.lower() in blog['blog'].titre.lower()]
        return {
            "search":search,
            "blogs":blogs_filter
        }
    
    if categorie:
        blogs_filter = [blog for blog in blogs_filter if categorie.lower() in blog['categories']]
        return {
            "search":search,
            "blogs":blogs_filter
        }
    return blogs_filter


#Recuperer un blog précis
@router.get('/{blog_id}', status_code=status.HTTP_200_OK)
async def getBlog(blog_id:int, db:Session = Depends(getSession)):
    
    blog = db.get(Blog, blog_id)
    
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog non trouvé")
    
    return {
        'blog':blog,
        'categories':blog.categories
    }


#Ajout d'un blog
@router.post('/', status_code=status.HTTP_201_CREATED)
async def createBlog(create_blog:BlogRequest, user:user_dependency, db: Session = Depends(getSession)):
    
    blog = Blog(
        titre=create_blog.titre,
        date=create_blog.date,
        published=False,
        utilisateur_id=user.get('id'),
    )
    
    for categorie_id in create_blog.categories:
        categorie = db.get(Categorie, categorie_id)
        blog.categories.append(categorie)
        
    db.add(blog)
    db.commit()


#Modifier un blog
@router.put('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
async def updateBlog(blog_id: int,update_blog: BlogRequest, user: user_dependency, db: Session = Depends(getSession)):
    blog = db.exec(select(Blog).where(Blog.id == blog_id)).first()
    
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog non trouvé")

    blog.titre = update_blog.titre
    blog.published = update_blog.published
    blog.date = update_blog.date
    
    for categorie_id in update_blog.categories:
        categorie = db.get(Categorie, categorie_id)
        blog.categories.append(categorie)
        
    db.commit()


#Supprimer un blog
@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleteBlog(blog_id:int, user:user_dependency, db: Session = Depends(getSession)):
    
    blog = db.exec(select(Blog).where(Blog.id == blog_id)).first()
    
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog non trouvé")
    
    db.delete(blog)
    db.commit()
    