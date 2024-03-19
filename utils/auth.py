from http.client import HTTPException
import os
from datetime import timedelta, datetime, timezone
import jwt
from security import hash_token
from jose import JWTError
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    # data {"email": "email"}
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire, "time": datetime.now(timezone.utc).timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #     save to db in hash
    #     save_token(hash_token(encoded_jwt))
    return encoded_jwt

async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception
        # if( find_token(hash_token(token)))  == None):
        #    raise credentials_exception
        username
    except JWTError:
        # dele_token{"hash": hash_token(token)}
        raise credentials_exception
    # user = get_user(email=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user