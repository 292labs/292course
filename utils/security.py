import hashlib
import secrets


def hash_password(password, salt=None):
    if salt:
        password = password + salt
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash, salt=None):
    if salt:
        password = password + salt
    return hash_password(password) == hash

def generate_salt():
    return secrets.token_hex(32)

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()