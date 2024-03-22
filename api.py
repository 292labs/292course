from __main__ import app
from flask import request
from flask_restful import Resource, Api
from utils.auth import create_access_token, get_current_user, create_stream_token
from utils.db_handler import user_exists, get_user, save_user, delete_token, get_courses, get_lessons, get_advancements, save_stream_token, get_stream_tokens
from utils.security import generate_salt, hash_password, verify_password, hash_token

api = Api(app)

# courses + add by admin
# advancments + add by admin
# lessons + add by admin
#

class Login(Resource):
    def get(self, request_ = None):

        if request_ is None: 
            request_ = request
        
        email = request_.form["email"]
        password = request_.form["password"]
        user = get_user(email)
        if user is None:
            return {"status": "failed", "message": "Invalid credentials"}
        
        salt = user[6]
        hash = user[2]

        if verify_password(password, hash, salt):
            token = create_access_token({"email": email})
            return {"status": "success", "token": token, "token_type": "bearer"}
        else:
            return {"status": "failed", "message": "Invalid credentials"}

class Signup(Resource):   
    def post(self, request_ = None):

        if request_ is None: 
            request_ = request

        email = request_.form["email"]
        password = request_.form["password"]
        birthdate = request_.form["birthdate"]
        name = request_.form["name"]
        last_name = request_.form["last_name"]
            
        if user_exists(email): 
            return {"status": "failed", "message": "User already exists"}
            
        salt = generate_salt()
        hash = hash_password(password, salt)
        save_user(email, hash, salt, birthdate, name=[name, last_name])
        user = get_user(email)

        token = create_access_token({"email": email})

        return {"status": "success", "token": token, "token_type": "bearer"} 
    
class Refresh(Resource):   
    def post(self, request_ = None):
        if request_ is None: 
            request_ = request

        token = request_.form["token"]
        if token is None:
           return {"status": "failed", "message": "Invalid token"}
        delete_token(hash_token(token))
        user = get_current_user(token) # returns user data from database
        token = create_access_token({"email": user["email"]})
        return {"status": "success", "token": token}

class TokenLogin(Resource): 
    def post(self, request_ = None):
        if request_ is None: 
            request_ = request

        token = request_.form["token"]
        
        if token is None:
            return {"status": "failed", "message": "Invalid token"}
    
        user = get_current_user(token)
    
        if user is None:
            return {"status": "failed", "message": "Invalid token"}
       
        return {"status": "success", "message": user}
        
class Courses(Resource):
    def get(self):
        cources = get_courses()
        return {"status": "success", "message": cources}

class Lessons(Resource):
    def get(self, request_ = None):
        if request_ is None: 
            request_ = request

        token = request_.form["token"]
        course_id = request_.form["course_id"]

        if token is None:
            return {"status": "failed", "message": "Invalid token"}
        
        user = get_current_user(token)
        
        if course_id not in user[4]:
            return {"status": "failed", "message": "Invalid course id or lack of permissions"}
        
        lessons = get_lessons(course_id)

        return {"status": "success", "message": lessons}
        
class Advancments(Resource):
    def get(self, request_ = None):
        if request_ is None: 
            request_ = request

        token = request_.form["token"]
        amount = request_.form["amount"] # all, anlocked, locked

        if token is None:
            return {"status": "failed", "message": "Invalid token"}
        
        user = get_current_user(token)

        if amount not in ["all", "unlocked", "locked"]:
            return {"status": "failed", "message": "Invalid amount"}
        
        advancments = get_advancements(user[5], amount)
        return {"status": "success", "message": advancments}

class StreamTokens(Resource):
    def post(self, request_ = None):
        if request_ is None: 
            request_ = request

        course = request_.form["course_id"]
        author = request_.form["author_id"]
        
        user = get_current_user(token)

        if user[3] not in [2, 3]:
            token = create_stream_token()
            save_stream_token(token, course, author)
            return {"status": "success", "message": token}
        else:
            return {"status": "failed", "message": "Invalid permissions"}
        
    def get(self, request_ = None):
        if request_ is None: 
            request_ = request

        token = request_.form["token"]
        course = request_.form["course_id"]
        
        user = get_current_user(token)

        if user[3] not in [2, 3] or course not in user[4]:
            token = get_stream_tokens(course)
            return {"status": "success", "message": token}
        else:
            return {"status": "failed", "message": "Invalid permissions"}



    
api.add_resource(Login, "/api/v1/auth/login")
api.add_resource(Signup, "/api/v1/auth/signup")
api.add_resource(Refresh, "/api/v1/auth/refresh")
api.add_resource(TokenLogin, "/api/v1/auth/login/token", "/api/v1/user/me")
api.add_resource(Courses, "/api/v1/courses/list")
api.add_resource(Lessons, "/api/v1/courses/lessons")
api.add_resource(Advancments, "/api/v1/user/advancments")
