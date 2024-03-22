from __main__ import app
from flask import request
from flask_restful import Resource, Api
from utils.auth import create_access_token, get_current_user, create_stream_token
from utils.db_handler import user_exists, get_user, save_user, delete_token, \
    get_courses, get_lessons, get_advancements, save_stream_token, get_stream_tokens, \
    save_course, save_lesson, save_advancement, get_homework
from utils.security import generate_salt, hash_password, verify_password, hash_token

api = Api(app)


class Login(Resource):
    def get(self, request_=None):

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
    def post(self, request_=None):

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

        token = create_access_token({"email": email})

        return {"status": "success", "token": token, "token_type": "bearer"}


class Refresh(Resource):
    def post(self, request_=None, token_=None):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
        except:
            token = token_

        if token is None:
            return {"status": "failed", "message": "Invalid token"}
        user = get_current_user(token)  # returns user data from database

        if user is None:
            return {"status": "failed", "message": "Invalid token"}
        delete_token(hash_token(token))
        token = create_access_token({"email": user[5]})
        return {"status": "success", "token": token}


class TokenLogin(Resource):
    def post(self, request_=None, token_=None):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
        except:
            token = token_

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

    def post(self, request_=None,
             data={
                 "token": None,
                 "name": None,
                 "description": None,
                 "tech_stack": None,
                 "price": None,
                 "author": None,
                 "lessons_amount": None
             }):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
            name = request_.form["name"]
            description = request_.form["description"]
            tech_stack = request_.form["tech_stack"]
            price = request_.form["price"]
            author = request_.form["teacher_id"]
            lessons_amount = request_.form["lessons_amount"]
        except:
            token = data["token"]
            name = data["name"]
            description = data["description"]
            tech_stack = data["tech_stack"]
            price = data["price"]
            author = data["teacher_id"]
            lessons_amount = data["lessons_amount"]

        user = get_current_user(token)

        if user[3] in [2, 3]:
            save_course(name, description, tech_stack,
                        author, price, lessons_amount)
            return {"status": "success", "message": "Course created"}
        else:
            return {"status": "failed", "message": "Invalid permissions"}


class Lessons(Resource):
    def get(self, request_=None, data={"token": None, "course_id": None}):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
            course_id = request_.form["course_id"]
        except:
            token = data["token"]
            course_id = data["course_id"]

        if token is None:
            return {"status": "failed", "message": "Invalid token"}

        user = get_current_user(token)

        if int(course_id) not in user[4]:
            return {"status": "failed", "message": "Invalid course id or lack of permissions"}

        lessons = get_lessons(course_id)

        return {"status": "success", "message": lessons}

    def post(self, request_=None, data={
        "token": None,
        "course_id": None,
        "name": None,
        "description": None,
        "author": None,
        "content": None
    }):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
            course_id = request_.form["course_id"]
            name = request_.form["name"]
            description = request_.form["description"]
            author = request_.form["author_id"]
            content = request_.form["content"]
        except:
            token = data["token"]
            course_id = data["course_id"]
            name = data["name"]
            description = data["description"]
            author = data["author_id"]
            content = data["content"]

        user = get_current_user(token)

        if user[3] in [2, 3]:
            save_lesson(course_id, name, description, author, content)
            return {"status": "success", "message": "Lesson created"}
        else:
            return {"status": "failed", "message": "Invalid permissions"}


class Advancments(Resource):
    def get(self, request_=None, data={"token": None, "amount": None}):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
            amount = request_.form["amount"]  # all, anlocked, locked
        except:
            token = data["token"]
            amount = data["amount"]

        if token is None:
            return {"status": "failed", "message": "Invalid token"}


        user = get_current_user(token)

        if amount not in ["all", "unlocked", "locked"]:
            return {"status": "failed", "message": "Invalid amount"}

        advancments = get_advancements(user[5], amount)
        return {"status": "success", "message": advancments}

    def post(self, request_=None, data={
        "token": None,
        "course_id": None,
        "description": None,
            "name": None}):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
            course_id = request_.form["course_id"]
            description = request_.form["description"]
            name = request_.form["name"]
        except:
            token = data["token"]
            course_id = data["course_id"]
            description = data["description"]
            name = data["name"]

        user = get_current_user(token)

        if user[3] in [2, 3]:
            save_advancement(course_id, name, description)
            return {"status": "success", "message": "Advancment added"}
        else:
            return {"status": "failed", "message": "Invalid permissions"}


class StreamTokens(Resource):
    def post(self, request_=None, data={"course": None, "token": None, "author": None}):
        if request_ is None:
            request_ = request

        try:
            course = request_.form["course_id"]
            token = request_.form["token"]
            author = request_.form["author_id"]
        except:
            course = data["course_id"]
            token = data["token"]
            author = data["author_id"]


        user = get_current_user(token)

        if user[3] in [2, 3]:
            token = create_stream_token()
            save_stream_token(token, course, author)
            return {"status": "success", "message": token}
        else:
            return {"status": "failed", "message": "Invalid permissions"}

    def get(self, request_=None, data={"course": None, "token": None}):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
            course = request_.form["course_id"]
        except:
            token = data["token"]
            course = data["course"]

        user = get_current_user(token)

        if user[3] in [2, 3] or course not in user[4]:
            token = get_stream_tokens(course)
            return {"status": "success", "message": token}
        else:
            return {"status": "failed", "message": "Invalid permissions"}


class HomeWork(Resource):
    def get(self, request_=None, token_=None):
        if request_ is None:
            request_ = request

        try:
            token = request_.form["token"]
        except:
            token = token_

        user = get_current_user(token)

        if user is None:
            return {"status": "failed", "message": "Invalid token"}
        
        try:
            user_courses = user[4]
            all_lessons = []
            for course in user_courses:
                lessons = get_lessons(course_id=course)
                all_lessons += lessons

            all_homework = []
            for lesson in all_lessons:
                homework = get_homework(lesson[0])
                all_homework += homework

            return {"status": "success", "message": all_homework}
        except:

            return {"status": "failed", "message": "Invalid token"}


api.add_resource(Login, "/api/v1/auth/login")
"""
Endpoint: /api/v1/auth/login
Method: GET
Data Received: 
- email (string): The email of the user
- password (string): The password of the user

Possible Responses:
- Success: 
    - status: "success"
    - token: The access token for the user
    - token_type: "bearer"
- Failure:
    - status: "failed"
    - message: "Invalid credentials"
"""

api.add_resource(Signup, "/api/v1/auth/signup")
"""
Endpoint: /api/v1/auth/signup
Method: POST
Data Received: 
- email (string): The email of the user
- password (string): The password of the user
- birthdate (string): The birthdate of the user
- name (string): The name of the user
- last_name (string): The last name of the user

Possible Responses:
- Success: 
    - status: "success"
    - token: The access token for the user
    - token_type: "bearer"
- Failure:
    - status: "failed"
    - message: "User already exists"
"""

api.add_resource(Refresh, "/api/v1/auth/refresh")
"""
Endpoint: /api/v1/auth/refresh
Method: POST
Data Received: 
- token (string): The refresh token

Possible Responses:
- Success: 
    - status: "success"
    - token: The new access token for the user
- Failure:
    - status: "failed"
    - message: "Invalid token"
"""

api.add_resource(TokenLogin, "/api/v1/auth/login/token", "/api/v1/user/me")
"""
Endpoint: /api/v1/auth/login/token, /api/v1/user/me
Method: POST
Data Received: 
- token (string): The access token

Possible Responses:
- Success: 
    - status: "success"
    - message: The user data
- Failure:
    - status: "failed"
    - message: "Invalid token"
"""

api.add_resource(Courses, "/api/v1/courses/list")
"""
Endpoint: /api/v1/courses/list
Method: GET, POST
Data Received (POST):
- token (string): The access token
- name (string): The name of the course
- description (string): The description of the course
- tech_stack (string): The tech stack of the course
- price (string): The price of the course
- author (string): The ID of the teacher
- lessons_amount (string): The amount of lessons in the course

Possible Responses:
- Success (GET): 
    - status: "success"
    - message: The list of courses
- Success (POST):
    - status: "success"
    - message: "Course created"
- Failure:
    - status: "failed"
    - message: "Invalid permissions"
"""

api.add_resource(Lessons, "/api/v1/courses/lessons")
"""
Endpoint: /api/v1/courses/lessons
Method: GET, POST
Data Received (GET):
- token (string): The access token
- course_id (string): The ID of the course

Data Received (POST):
- token (string): The access token
- course_id (string): The ID of the course
- name (string): The name of the lesson
- description (string): The description of the lesson
- author (string): The ID of the author
- content (string): The content of the lesson

Possible Responses:
- Success (GET): 
    - status: "success"
    - message: The list of lessons
- Success (POST):
    - status: "success"
    - message: "Lesson created"
- Failure:
    - status: "failed"
    - message: "Invalid permissions" or "Invalid course id or lack of permissions"
"""

api.add_resource(Advancments, "/api/v1/user/advancments")
"""
Endpoint: /api/v1/user/advancments
Method: GET, POST
Data Received (GET):
- token (string): The access token
- amount (string): The amount of advancements to retrieve ("all", "unlocked", "locked")

Data Received (POST):
- token (string): The access token
- course_id (string): The ID of the course
- description (string): The description of the advancement
- name (string): The name of the advancement

Possible Responses:
- Success (GET): 
    - status: "success"
    - message: The list of advancements
- Success (POST):
    - status: "success"
    - message: "Advancement added"
- Failure:
    - status: "failed"
    - message: "Invalid permissions" or "Invalid amount"
"""

api.add_resource(StreamTokens, "/api/v1/stream/token", "/api/v1/stream/list")
"""
Endpoint: /api/v1/stream/token, /api/v1/stream/list
Method: POST, GET
Data Received (POST):
- course (string): The ID of the course
- token (string): The access token
- author (string): The ID of the author

Data Received (GET):
- token (string): The access token
- course (string): The ID of the course

Possible Responses:
- Success (POST): 
    - status: "success"
    - message: The stream token
- Success (GET):
    - status: "success"
    - message: The stream tokens
- Failure:
    - status: "failed"
    - message: "Invalid permissions"
"""

api.add_resource(HomeWork, "/api/v1/user/homework")
"""
Endpoint: /api/v1/user/homework
Method: GET
Data Received:
- token (string): The access token

Possible Responses:
- Success:
    - status: "success"
    - message: The list of homework
- Failure:
    - status: "failed"
    - message: "Invalid token"
"""
