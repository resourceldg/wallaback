import os
import jwt

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
#os.getenv['SECRET']  




class AuthHandler():
    
    # Creamos las instancias de clase algunas importaciones que vamos a utilizar
    
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret ="SECRET"

    
    # Obtiene el valor de la contraseña en texto plano y devolverá una hasheada
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    # Compara de el pass en texto plano con el hesheado y devuelve true si se correspnde la igualdad
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # Creamos el jwt aceptando por parametro el id que usamos con asunto del token,
    # usamos timedelta para setearlo en 5 min y tb visualizar problmas de expiracion y otras yerbas...
    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        # Creamos el token con nuestro secreto
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    # Decodificamos el token
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')
   

    # SECURITY SQLI Para protegernos de una una inyección SQL esto ASEGURA de que se haya sumistrado el token
    #  de portador del encabezado de autenticación http, pero no hace nada para validarlo, SOLO REVISA SU PRESENCIA AQUÍ,
    #  luego nosotros mismos nos encargamos de validarlo.
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
