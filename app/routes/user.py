
from auth.auth import AuthHandler
from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.sql.expression import select
from config.db import conn
from models.user import users
from schema.user import User
from cryptography.fernet import Fernet

# get instance by imports

user = APIRouter()
auth_handler = AuthHandler()
key= Fernet.generate_key()
f = Fernet(key)


@user.post("/login", tags=["users"])
async def login (email:str,password:str):
    #login user
    r = conn.execute(users.select().where(users.c.email == email)).first()#check if email exist
    
    """ print(r.password)
    print(password) """
  
    if (r):
        if  auth_handler.verify_password(password, r.password):
            token = auth_handler.encode_token(r.name)
            print('Login successfully!')
            return { 'token': token } 
        else:
            raise HTTPException(status_code=401, detail='LOGIN ERROR: Invalid email and/or password')
    else: 
        raise HTTPException(status_code=404, detail="LOGIN ERROR: Email not found")


@user.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@user.get('/protected')
def protected(name=Depends(auth_handler.auth_wrapper)):
    return { 'name': name}

@user.get("/users", tags=["users"])
async def get_users():
    #get all users
    return conn.execute(users.select()).fetchall()

@user.post("/users", tags=["users"])
async def create_users(user:User):
    #create user by eschema
    valid = conn.execute(users.select().where(users.c.email == user.email)).first()#check if email exist
    if (not valid):
        new_user= {'name': user.name, 'email': user.email}
        #new_user['password']= f.encrypt(user.password.encode('utf-8'))
        hashed_password = auth_handler.get_password_hash(user.password)
        new_user['password']= hashed_password
        result= conn.execute(users.insert().values(new_user))
        print('User created successfully!')
        return conn.execute(users.select().where(users.c.id == result.inserted_primary_key[0])).first()
    else: 
        raise HTTPException(status_code=403, detail="CREATION ERROR: Email already exist")

@user.get("/users/{id}", tags=["users"])
async def get_user(id:str):
    #search user by id
    valid = conn.execute(users.select().where(users.c.id == id)).first()#check if id exist
    if (valid):
        result = conn.execute(users.select().where(users.c.id == id)).first()
        print('User found successfully!')
        return result
    else: 
        raise HTTPException(status_code=404, detail="SEARCH ERROR: User id not found")

@user.delete("/users/{id}", tags=["users"])
async def delete_user(id:str):
    #delete user by id
    valid = conn.execute(users.select().where(users.c.id == id)).first()#check if id exist
    if (valid):
        result= conn.execute(users.delete().where(users.c.id == id))
        print(result)
        return 'User deleted successfully!'
    else: 
        raise HTTPException(status_code=404, detail="DELETE ERROR: User id not exist")
        
@user.put("/users/{id}", tags=["users"])
async def update_user(id:str, user:User):
    #update user by id
    valid = conn.execute(users.select().where(users.c.id == id)).first()#check if id exist
    if (valid):
        result= conn.execute(users.update().values(name= user.name, email= user.email,
        password= f.encrypt(user.password.encode('utf-8'))).where(users.c.id == id))
        print(result)
        return 'User update successfully!'
    else: 
        raise HTTPException(status_code=404, detail="UPDATE ERROR: User id not exist")







        