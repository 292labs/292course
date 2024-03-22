from flask import Flask, render_template, request, make_response

app = Flask(__name__)

import api


@app.route("/")
def hello_world():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":
        response = api.Login().get(request_=request)
        print(response)
        if response["status"] == "success":
            token = response["token"]
            resp = make_response(render_template("main.html"))
            resp.set_cookie("token", token, secure=True, httponly=True)

            return resp
        else:
            return render_template("login.html")
        
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        response = api.Signup().post()

        if response["status"] == "success":
             token = response["token"]
             resp = make_response(render_template("main.html"))
             resp.set_cookie("token", token, secure=True, httponly=True)
             return resp
        else:
             return render_template("signup.html")


    return render_template("signup.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
