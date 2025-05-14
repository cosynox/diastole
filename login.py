from flask import redirect, render_template, request, session
from flask_babel import lazy_gettext as _l
from dbaccess import getDB
from helpers import apology
from werkzeug.security import check_password_hash, generate_password_hash

def user_login():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology(_l("must provide username"), 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology(_l("must provide password"), 400)

        conn = getDB()
        cur = conn.cursor()

        # Query database for username
        username = request.form.get("username")
        cur.execute("SELECT id, pwhash FROM users WHERE username = ?", (username,))
        rows = cur.fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][1], request.form.get("password")
        ):
            return apology(_l("invalid username and/or password"), 400)
        
        cur.execute("UPDATE users SET retries = 0, last_login = current_timestamp WHERE id = ? LIMIT 1", (rows[0][0],)) 
        conn.commit()
        conn.close()
        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/diastole")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

def user_register():
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology(_l("must provide username"), 400)

        conn = getDB()
        cur = conn.cursor()

        if len(username) > 0:
            cur.execute("SELECT id FROM users WHERE username = ?", (username,))
            rows = cur.fetchall()
            if len(rows) > 0:
                return apology(_l("username is already registered"), 400)
        # ok, username is valid

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology(_l("must provide password"), 400)

        if len(password) < 1:
            return apology(_l("empty password not allowed"), 400)
        # ok, password is valid

        # Ensure password confirmation was submitted
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology(_l("must provide confirmation of password"), 400)

        if confirmation != password:
            return apology(_l("Your password and the confirmation do not match"), 400)
        # confirmation is ok

        pwhash = generate_password_hash(password)

        # insert new user
        cur.execute(
            "INSERT INTO users (username, pwhash) values (?, ?)", (username, pwhash,))
        conn.commit()
        conn.close()
        # Redirect user to home page
        return redirect("/diastole")

    return render_template("register.html")

def user_pwchange():
    try:
        userid = int( session["user_id"] )
    except (TypeError, ValueError):
        return apology(_l("session data corrupted"), 400)
    
    conn = getDB()
    if request.method == "POST":
        # Ensure username was submitted
        cur = conn.cursor()

        if userid > 0:
            cur.execute("SELECT id FROM users WHERE id = ?", (userid,))
            rows = cur.fetchall()
            if len(rows) > 1:
                return apology(_l("duplicate userid"), 400)
            elif len(rows) == 0:
                return apology(_l("userid not found"), 400)

        # ok, userid is valid

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology(_l("must provide password"), 400)

        if len(password) < 1:
            return apology(_l("empty password not allowed"), 400)
        # ok, password is valid

        # Ensure password confirmation was submitted
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology(_l("must provide confirmation of password"), 400)

        if confirmation != password:
            return apology(_l("Your password and the confirmation do not match"), 400)
        # confirmation is ok

        pwhash = generate_password_hash(password)

        # insert new user
        cur.execute(
            "UPDATE users SET pwhash = ? WHERE id = ? LIMIT 1", (pwhash,userid,))
        conn.commit()
        conn.close()
        # Redirect user to home page
        return redirect("/diastole")

    return render_template("pwchange.html")
