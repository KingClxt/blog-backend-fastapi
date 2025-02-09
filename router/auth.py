from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from models.Utilisateur import Utilisateur
from dependencies.db import getSession
from dependencies.auth import bcrypt, authenticate, create_token
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

@router.post('/inscription')
async def inscription(create_user: Utilisateur, db:Session = Depends(getSession)):
    utilisateur = Utilisateur(
        nom=create_user.nom,
        prenom=create_user.prenom,
        email=create_user.email,
        role="",
        tel=create_user.tel,
        mot_de_passe=bcrypt.hash(create_user.mot_de_passe)    
    )
    db.add(utilisateur)
    db.commit()

# Authentification
@router.post('/token')
async def create_access_token(formData: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(getSession)):
    user = authenticate(formData.username, formData.password, db)
    if user is None:
        raise HTTPException(status_code=404, detail="Erreur lors de la connexion")
    token = create_token(user.email, user.id, user.role, timedelta(hours=1))
    return {
        'access_token':token,
        'type':'bearer'
    }
    