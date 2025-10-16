from flask import flash

def validate_signup(username, password1, password2):
    fail = False
    errors = []

    if len(username) > 30 or len(username) < 1:
        errors.append("Username is invalid length")
        fail = True

    if password1 != password2:
        errors.append("Passwords do not match.")
        fail = True

    if len(password1) < 10:
        errors.append("Password has to be at least 10 characters long.")
        fail = True

    if fail:
        for error in errors:
            flash(error)
        raise ValueError
    return

def validate_new_log(title, author, status, rating, review):
    fail = False
    errors = []

    if len(title) > 500 or len(title.strip()) == 0:
        errors.append("Title is missing or too long")
        fail = True

    if len(author) > 300 or len(author.strip()) == 0:
        errors.append("Author is missing or too long")
        fail = True

    if status not in ["want-to-read", "reading", "read", "dropped", "on-hold"]:
        errors.append("Invalid status")
        fail = True

    if rating != "":
        if int(rating) not in range(1, 11):
            errors.append("Invalid rating")
            fail = True

    if len(review) > 10000:
        errors.append("Review has to be less than 10000 characters")
        fail =True

    if fail:
        for error in errors:
            flash(error)
        raise ValueError
    return

def validate_log_update(status, rating, review):
    fail = False
    errors = []

    if status not in ["want-to-read", "reading", "read", "dropped", "on-hold"]:
        errors.append("Invalid status")
        fail = True

    if rating != "":
        if not rating.isdigit() or int(rating) not in range(1, 11):
            errors.append("Invalid rating")
            fail = True

    if len(review) > 10000:
        errors.append("Review has to be less than 10000 characters")
        fail =True

    if fail:
        for error in errors:
            flash(error)
        raise ValueError
    return
