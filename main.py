from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("main.html")


@app.route("/login")
def login_page():
        
    return render_template("login.html")


@app.route("/signup")
def signup_page():

    return render_template("signup.html")

@app.route("/dashboard")
def dashboard_page():

    return render_template("dashboard.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
