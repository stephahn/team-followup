import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required
# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    """Display about this site page"""
    # downloading the data of user ID from SQLlite table
    return render_template("index.html")


@app.route("/projects", methods=["GET"])
@login_required
def projects():
    """Display about this site page"""
    # downloading the data of user ID from SQLlite table
    return render_template("projects.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # aquiring log in data from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # check if username already exists or the existence of an username
        username_check = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(username) == 0:
            return apology("Please enter an username")
        elif len(username_check) != 0:
            return apology("username already in use")
        elif username == db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("username already in use")

        # check password matching or if there is a password
        elif len(password) == 0:
            return apology("Please enter a password")
        elif password != confirm_password:
            return apology("password doesn't match")
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # logs in the users and adds him to the cookies
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")


@app.route("/newPatient", methods=["GET"])
@login_required
def newPatient():
    if request.method == "GET":
        return render_template("newPatient.html")



@app.route("/examinations", methods=["GET"])
@login_required
def examinations():
    if request.method == "GET":
        return render_template("examinations.html")


@app.route("/patients", methods=["GET"])
@login_required
def patients():
    if request.method == "GET":
        return render_template("patients.html")

