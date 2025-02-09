from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from dependencies.db import getSession
from models.Categorie import Categorie
from starlette import status
from dependencies.auth import user_dependency

router = APIRouter(
    prefix="/categories",
    tags=["CATEGORIES"]
)

@router.get('/', status_code=status.HTTP_200_OK)
async def getAllCategories(db:Session = Depends(getSession)):
    blogs = db.exec(select(Categorie)).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
async def createCategorie(create_caegorie: Categorie,user:user_dependency, db: Session = Depends(getSession)):
    categorie = Categorie(**create_caegorie.model_dump())
    db.add(categorie)
    db.commit()


@router.put('/{id_categorie}')
async def updateCategorie(id_categorie:int ,update_categorie: Categorie, db: Session = Depends(getSession)):
    categorie = db.exec(select(Categorie).where(Categorie.id == id_categorie)).one()
    if categorie is None:
        raise HTTPException(status_code=404, detail="Categorie non trouvé")
    categorie.titre = update_categorie.titre
    db.commit()
    db.refresh(categorie)
    return categorie


@router.delete('/{id_categorie}', status_code=status.HTTP_204_NO_CONTENT)
async def deleteCategorie(id_categorie:int, db:Session = Depends(getSession)):
    
    categorie = db.get(Categorie, id_categorie)
    if categorie is None:
        raise HTTPException(status_code=404, detail="Categorie non trouvé")
    
    db.delete(categorie)
    db.commit()
    
    return {"message":"suppression terminer!"}