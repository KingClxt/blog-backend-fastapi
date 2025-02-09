from datetime import timedelta, datetime, timezone
from typing import Annotated
from passlib.context import CryptContext
from sqlmodel import select, Session
from models.Utilisateur import Utilisateur
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer


bcrypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = '0192347b144520fd77b7d5973506094f9f67f5aae9a666b274e026a602ca667b'
ALGO = 'HS256'
oauth_2password_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


# Verification JWT
def get_current_user(token: Annotated[str, Depends(oauth_2password_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGO)
        email = payload.get('email')
        id = payload.get('id')
        role = payload.get('role')
        
        if email is None or id is None or role is None:
            raise HTTPException(status_code=401, detail="Vous n'etes pas autoriser a acceder a cette url")
        return {'email':email, 'id':id, 'role':role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Erreur jwt")


# Verification de l'email et du mot de passe de l'utilisateur
def authenticate(email, password, db:Session):
    utilisateur = db.exec(select(Utilisateur).where(Utilisateur.email == email)).first()
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Email incorrecte")

    if not bcrypt.verify(password, utilisateur.mot_de_passe):
        raise HTTPException(status_code=404, detail="Mot de passe incorrecte")
    
    return utilisateur

# Création du jéton jwt
def create_token(email, id, role, expire: timedelta):
    encode = {
        'email':email,
        'id':id,
        'role':role
    }
    expires = datetime.now(timezone.utc) + expire
    encode.update({'exp':expires})
    
    return jwt.encode(encode, SECRET_KEY, ALGO)

# Injection de dependance pour proteger mes routes et recuoerer en meme temps l'utilisateur associer au jwt
user_dependency = Annotated[dict, Depends(get_current_user)]