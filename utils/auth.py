import os
import jwt
import secrets
from http.client import HTTPException
from datetime import timedelta, datetime, timezone
from jose import JWTError
from utils.security import hash_token
from utils.db_handler import save_token, get_user, find_token, delete_token

SECRET_KEY = "our_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    # data {"email": "email"}
    expires_delta = timedelta(hours=31*24)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire, "time": datetime.now(timezone.utc).timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    user = get_user(email=to_encode["email"])
    save_token(user[0], encoded_jwt)

    return encoded_jwt

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")

        if email is None:
            delete_token(hash_token(token))
            return None
        if (find_token(hash_token(token)))  == None:
            return None
        
    except JWTError:
        delete_token(hash_token(token))
        return None
    user = get_user(email=email)
    if user is None:
        return None
    
    return user

def create_stream_token():
    return secrets.token_hex(16)