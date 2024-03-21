from http.client import HTTPException
import os
from datetime import timedelta, datetime, timezone
import jwt
from jose import JWTError

from utils.security import hash_token
from utils.db_handler import save_token, get_user, find_token, delete_token

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict, expires_delta: timedelta = None):
    # data {"email": "email"}
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

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("email")

    # probably add some code for token expiration

    if email is None:
        delete_token(hash_token(token))
        return None
    if (find_token(hash_token(token)))  == None:
        return None

    user = get_user(email=email)
    if user is None:
        return None
    
    return user