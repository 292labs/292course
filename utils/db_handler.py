import psycopg2
import os, datetime
from utils.security import hash_token


conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)


cur = conn.cursor()

# database

def save_user(email, password_hash, salt, birthdate, name:list):
    name_ = " ".join(name)
    age = calculate_age(birthdate=birthdate)
    cur.execute("""INSERT INTO "User" (username, role_id, password, salt, email, age) 
                VALUES (%s, %s, %s, %s, %s, %s);""", 
                (name_, 1, password_hash, salt, email, age))
    conn.commit()

def save_token(user_id, token):
    hash = hash_token(token)
    cur.execute("""INSERT INTO "Token" (user_id, token)
                VALUES  (%s, %s);""",
                (user_id, hash))
    conn.commit()

def get_user(email):
    cur.execute("""SELECT * FROM "User" WHERE email = %s""", [email])
    return cur.fetchone()

def user_exists(email):
    cur.execute("""SELECT 1 FROM "User" WHERE email = %s""", [email])
    return cur.fetchone() is not None

def find_token(token):
    cur.execute("""SELECT * FROM "Token" WHERE token = %s""", [token])
    return cur.fetchone()

def delete_token(hash):
    cur.execute("""DELETE FROM "Token" WHERE token = %s""", [hash])
    conn.commit()

def get_courses():
    cur.execute("""SELECT * FROM "Course" """)
    return cur.fetchall()

def get_lessons(course_id):
    cur.execute("""SELECT * FROM "Lessons" WHERE course_id = %s""", [str(course_id)])
    return cur.fetchall()

def get_advancements(email, amount="all"):
    user = get_user(email)
    user_achivments = user[7]

    if amount == "all":
        cur.execute("""SELECT * FROM "Advancements" WHERE course_id = %s""", [user[4]])
        return cur.fetchall()
    
    elif amount == "unlocked":
        return user_achivments

    elif amount == "locked":
        all_achivments = []
        if user[4] is not list:
            cur.execute("""SELECT * FROM "Advancements" WHERE course_id = %s""", [user[4][0]])
            all_achivments += cur.fetchall()
        else:
            for course in user[4]:
                cur.execute("""SELECT * FROM "Advancements" WHERE course_id = %s""", course[0])
                all_achivments += cur.fetchall()
        try:
            achivments = [achivment for achivment in all_achivments if achivment[0] not in user_achivments]
            return achivments
        except:
            return None
    
def save_stream_token(token, course_id, user_id):
    cur.execute("""INSERT INTO "StreamToken" (token, user_id, course_id)
                VALUES (%s, %s, %s);""", (token, user_id, course_id))
    conn.commit()

def get_stream_tokens(course_id):
    cur.execute("""SELECT * FROM "StreamToken" WHERE course_id = %s""", [course_id])
    return cur.fetchall()

def save_course(name, description, tech_stack, teacher_id, price, lessons_amount):
    cur.execute("""INSERT INTO "Course" (name, description, tech_stack, teacher_id, price, lessons)
                VALUES (%s, %s, %s, %s, %s, %s);""", (name, description, tech_stack, teacher_id, price, lessons_amount))
    conn.commit()

def save_lesson(course_id, name, description, author_id, content):
    cur.execute("""INSERT INTO "Lessons" (course_id, name, description, author_id, content)
                VALUES (%s, %s, %s, %s, %s);""", (course_id, name, description, author_id, content))
    conn.commit()

def save_advancement(course_id, name, description):
    cur.execute("""INSERT INTO "Advancements" (course_id, name, description)
                VALUES (%s, %s, %s);""", (course_id, name, description))
    conn.commit()

def get_homework(lesson_id):
    cur.execute("""SELECT * FROM "Homework" WHERE lesson_id = %s""", [lesson_id])
    return cur.fetchall()

# utility functions

def calculate_age(birthdate:str):
    born = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.date.today()
    try: 
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday.date() > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


