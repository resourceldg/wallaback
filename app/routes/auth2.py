from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi import APIRouter, HTTPException, Response, Depends, JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from config.db import conn
from models.user import users
from schema.user import User
from cryptography.fernet import Fernet

"""
By default, the CRSF cookies will be called csrf_access_token and
csrf_refresh_token, and in protected endpoints we will look
for the CSRF token in the 'X-CSRF-Token' headers. only certain
methods should define CSRF token in headers default is ('POST','PUT','PATCH','DELETE')
"""

user = APIRouter()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = False
    # Enable csrf double submit protection. default is True
    authjwt_cookie_csrf_protect: bool = True
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # authjwt_cookie_samesite: str = 'lax'

@AuthJWT.load_config
def get_config():
    return Settings()

@user.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@user.post('/login')
def login(email:str,password:str, Authorize: AuthJWT = Depends()):
    valid = conn.execute(users.select().where(users.c.email == email)).first()#check if email exist
    r= conn.execute(users.select().where(users.c.email == email)).first()
    """
    With authjwt_cookie_csrf_protect set to True, set_access_cookies() and
    set_refresh_cookies() will now also set the non-httponly CSRF cookies
    """
    if r.email != email or r.password != password:
        raise HTTPException(status_code=401,detail="Bad username or password")

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=r.name)
    refresh_token = Authorize.create_refresh_token(subject=r.name)

    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login"}

@user.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@user.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookie in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}

@user.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
