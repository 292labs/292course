from __main__ import app
from flask import request
from flask_restful import Resource, Api
from utils.auth import create_access_token

api = Api(app)


# /v1/user/me
# /v1/user/{id}

class Login(Resource):
    def get(self, request_ = None):

        if request_ is None: 
            request_ = request
        
        # email = request_.form["email"]
        # password = request_.form["password"]
        # hash = get_hash_password(email) # get hash from database
        # salt = get_salt(email) # get salt from database
        # if verify_password(password, hash, salt):
        #     token = create_access_token({"email": email})
        #     return {"status": "success", "token": token}
        # else:
        #     return {"status": "failed", "message": "Invalid credentials"}

class Signup(Resource):   
    def post(self, request_ = None):
        if request_ is None: 
            request_ = request
        # email = request_.form["email"]
        # password = request_.form["password"]
        # birthdate = request_.form["birthdate"]
        # name = request_.form["name"]
        # last_name = request_.form["last_name"]
            
        # if user_exists(email): 
        #    return {"status": "failed", "message": "User already exists"}
            
        # salt = generate_salt()
        # hash = hash_password(password, salt)
        # save_user(email, hash, salt, birthdate, name, last_name)
        # token = create_access_token({"email": email})
        # return {"status": "success", "token": token}
        

    
class Refresh(Resource):   
    def post(self, request_ = None):
        if request_ is None: 
            request_ = request

        # token = request_.form["token"]
        # if token is None:
        #    return {"status": "failed", "message": "Invalid token"}
        # user = get_current_user(token) # returns user data from database
        # token = create_access_token({"email": user["email"]})
        # return {"status": "success", "token": token}

class TokenLogin(Resource):    
    def post(self, request_ = None):
        if request_ is None: 
            request_ = request

        # token = request_.form["token"]
        # if token is None:
        #    return {"status": "failed", "message": "Invalid token"}
        # user = get_current_user(token) # returns user data from database
        # return {"status": "success", "message": user}
        

    
api.add_resource(Login, "/api/v1/auth/login")
api.add_resource(Signup, "/api/v1/auth/signup")
api.add_resource(Refresh, "/api/v1/auth/refresh")
api.add_resource(TokenLogin, "/api/v1/auth/login/token")