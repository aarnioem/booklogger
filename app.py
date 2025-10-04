import sqlite3

from flask import Flask
from flask import render_template, request, session, redirect, flash
from werkzeug.security import generate_password_hash

import config
import logs
import users
import forms

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    newest_logs = logs.get_all_logs()
    return render_template("index.html", newest_logs=newest_logs)

@app.route("/search")
def search():
    query = request.args.get("query")
    results = logs.search_by_title(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/new_log", methods=["GET", "POST"])
def new_log():
    users.check_login()

    if request.method == "GET":
        return render_template("new_log.html")

    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        title = request.form["title"]
        author = request.form["author"]
        status = request.form["status"]
        rating = request.form["rating"]
        review = request.form["review"]
        user_id = session["user_id"]

        try:
            forms.validate_new_log(title, author, status, rating, review)
        except ValueError:
            return redirect("/new_log")

        logs.add_log(title, author, status, rating, review, user_id)
        flash("New log created successfully")
        return redirect("/")

@app.route("/log/<int:log_id>")
def view_log(log_id):
    log = logs.get_log_by_id(log_id)
    comments = logs.get_comments_by_log_id(log_id)
    return render_template("view_log.html", book=log, comments=comments)

@app.route("/edit/<int:log_id>")
def edit_log(log_id):
    users.check_login()
    users.check_permission(session["user_id"], log_id)
    log = logs.get_log_by_id(log_id)
    return render_template("edit_log.html", book=log)

@app.route("/update_log", methods=["POST"])
def update_log():
    users.check_csrf(request.form["csrf_token"])
    status = request.form["status"]
    rating = request.form["rating"]
    review = request.form["review"]
    log_id = request.form["log_id"]

    users.check_permission(session["user_id"], log_id)

    try:
        forms.validate_log_update(status, rating, review)
    except ValueError:
        return redirect("/new_log")

    logs.update_log(status, rating, review, log_id)
    return redirect("/my_books")

@app.route("/delete/<int:log_id>")
def delete(log_id):
    log = logs.get_log_by_id(log_id)
    users.check_permission(session["user_id"], log_id)
    return render_template("delete.html", book=log)

@app.route("/delete_log", methods=["POST"])
def delete_log():
    users.check_csrf(request.form["csrf_token"])
    log_id = request.form["log_id"]
    users.check_permission(session["user_id"], log_id)
    logs.delete_log(log_id)
    return redirect("/my_books")

@app.route("/add_comment", methods=["POST"])
def add_comment():
    users.check_login()
    users.check_csrf(request.form["csrf_token"])

    log_id = request.form["log_id"]
    content = request.form["content"]
    user_id = session["user_id"]

    logs.add_comment(log_id, user_id, content)
    return redirect(f"/log/{log_id}")

@app.route("/delete_comment/<int:comment_id>")
def delete_comment(comment_id):
    users.check_login()
    owner_id = logs.comment_owner_id(comment_id)

    if owner_id != session["user_id"]:
        flash("You can only remove your own comments.")
    else:
        logs.delete_comment(comment_id)
        flash("Comment removed")

    return redirect(request.referrer)


@app.route("/my_books")
def my_books():
    users.check_login()
    books = logs.get_logs_by_user_id(session["user_id"])
    return render_template("my_books.html", books=books)

@app.route("/members")
def members():
    user_list = users.get_users()
    return render_template("members.html", user_list=user_list)

@app.route("/profile/<int:user_id>")
def profile(user_id):
    member = users.get_user(user_id)
    books = logs.get_logs_by_user_id(user_id)
    return render_template("profile.html", member=member, books=books)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        try:
            forms.validate_signup(username, password1, password2)
        except ValueError:
            return redirect("/register")

        password_hash = generate_password_hash(password1)

        try:
            users.create_account(username, password_hash)
            flash("Account created successfully.")
        except sqlite3.IntegrityError:
            flash("Error: Username taken.")
            return redirect("/register")

        users.login(username, password1)
        flash("Logged in.")
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            flash("Logged in.")
            return redirect("/")

        flash("Wrong username or password.")
        return redirect("/login")

@app.route("/logout")
def logout():
    if "username" in session:
        session.clear()
        flash("Logged out.")
    return redirect("/")
