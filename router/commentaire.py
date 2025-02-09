from sqlmodel import select, Session
from dependencies.db import getSession
from dependencies.auth import user_dependency
from models.Commentaire import Commentaire
from fastapi import APIRouter, Depends, HTTPException
from starlette import status


router = APIRouter(
    prefix='/commentaire',
    tags=["COMMENTAIRE"]
)

#Récuperer tous les commentaires de la base de donnée
@router.get('/', status_code=status.HTTP_200_OK)
async def getAllComments(db:Session = Depends(getSession)):
    commentaires = db.exec(select(Commentaire)).all()
    return commentaires

#Recuperer les commentaires de l'utilisateur
@router.get('/user', status_code=status.HTTP_200_OK)
async def getComment(user: user_dependency, db:Session = Depends(getSession)):
    commentaires = db.exec(select(Commentaire).where(Commentaire.id_utiliisateur == user.get('id')))
    return commentaires

#Ajouter un commentaire
@router.post('/', status_code=status.HTTP_201_CREATED)
async def createComment(create_comment:Commentaire, user: user_dependency, db:Session = Depends(getSession)):
    comment_model = Commentaire(
        commentaire=create_comment.commentaire,
        id_utiliisateur=user.get('id')
    )
    db.add(comment_model)
    db.commit()
    
#Modifier un commentaire
@router.put('/{commentaire_id}', status_code=status.HTTP_204_NO_CONTENT)
async def editComment(commentaire_id:int,update_comment: Commentaire, user: user_dependency, db:Session = Depends(getSession)):
    commentaire = db.get(Commentaire, commentaire_id)
    
    if commentaire is None:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    commentaire.commentaire = update_comment.commentaire
    db.commit()    

#Supprimer un commentaire
@router.delete('/{commentaire_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleteComment(commentaire_id:int, user: user_dependency, db:Session = Depends(getSession)):
    commentaire = db.get(Commentaire, commentaire_id)
    if commentaire is None:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    
    db.delete(commentaire)
    db.commit()