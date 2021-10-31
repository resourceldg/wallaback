""" from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.expression import select
from config.db import conn
from .auth import AuthHandler
from models.user import user
from schema.user import User




auth_handler = AuthHandler()
user = APIRouter()


# Una funcion de registro que devuelve un 201 si va todo ok o un 400 si el usuario esta tomado
@user.post('/register', status_code=201)
def register(user: User):
    if any(x['name'] == user.name for x in User):
        raise HTTPException(status_code=400, detail='name is taken')
    hashed_password = auth_handler.get_password_hash(user.password)
    User.append({
        'name': user.name,
        'password': hashed_password    
    })
    return


@user.post('/login')
def login(user: User):
    user = None
    for x in User:
        if x['name'] == user.name:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(user.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid name and/or password')
    token = auth_handler.encode_token(user['name'])
    return { 'token': token }


@user.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@user.get('/protected')
def protected(name=Depends(auth_handler.auth_wrapper)):
    return { 'name': name }
 """