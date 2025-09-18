from flask import Flask
from flask import render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_log", methods=["GET", "POST"])
def new_log():
    if request.method == "GET":
        return render_template("new_log.html")
    
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        status = request.form["status"]
        rating = request.form["rating"]
        review = request.form["review"]

        sql = "INSERT INTO books (user_id, title, author, status, rating, review) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute(sql, [session['user_id'], title, author, status, rating, review])

        return "Book logged"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return "Error: Passwords do not match."
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            return "Error: Username taken"

        return "Account created" 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password_hash, id FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]
        
        sql = "SELECT password_hash, id FROM users WHERE username = ?"
        query = db.query(sql, [username])[0]
        password_hash = query[0]
        user_id = query[1]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "Error: Wrong username or password"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")