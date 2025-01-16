import jwt, datetime
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from rest_framework import exceptions
import os
import sys

# Agrega el directorio raíz del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from users.models import User
from dotenv import load_dotenv
import os

# Cargar el archivo .env
ruta = os.getcwd()
load_dotenv(ruta+"/cred.env")

SECRET_KEY = os.getenv("secret")


@database_sync_to_async
def get_user_by_token(token_key):
    try:
        print(type(token_key))
        id = decode_access_token(token_key)[0]
        print("primiiiiiiiiiikoooooooooooooooooooooo")
        print(User.objects.get(pk=id))
        return User.objects.get(pk=id)
    except Token.DoesNotExist:
        return None

class WebSocketTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        authorization_header = None
        #print(str(scope["query_string"]).split("token=")[1])
        if scope["query_string"]:
            authorization_header = str(scope["query_string"]).split("token=")[1].replace("'","")
        else:
            for header_name, header_value in scope["headers"]:
                if header_name == b"authorization":
                    authorization_header = header_value.decode("utf-8")
                    print("JOOOOOOOOOOOOOOOJOJOJOJOJOJ")
                    print(authorization_header)
                    break
        print(authorization_header)
        if authorization_header:
            token_key = authorization_header.split()[-1]
            print(token_key)
            user = await get_user_by_token(token_key)
            print(user)
            if user:
                scope["user"] = user

        return await super().__call__(scope, receive, send)




def create_access_token(id,email):
    return jwt.encode({
        'user_id': id,
        'email':email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=55),
        'iat': datetime.datetime.utcnow()
    }, SECRET_KEY,algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms='HS256')
        print(payload)
        return payload['user_id'],payload['username']
    except:
        raise exceptions.AuthenticationFailed('Desautentificado!! jiji')

def create_refresh_token(id,email):
    return jwt.encode({
        'user_id': id,
        'email':email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }, SECRET_KEY,algorithm='HS256')


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        return payload['user_id'],payload['email']
    except:
        raise exceptions.AuthenticationFailed('Desautentificado!! jeje')