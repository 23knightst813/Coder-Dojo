# auth.py
from flask import session, flash, redirect
from db import get_db_connection
from werkzeug.security import check_password_hash

def sign_in(email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """SELECT email, password, is_admin FROM users WHERE email = ?"""
    cur.execute(query, (email,))
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        session["email"] = user[0]  # Email
        session["is_admin"] = bool(user[2])  # is_admin
        if session["is_admin"]:
            return redirect("/admin")
        return redirect("/")
    else:
        flash("Invalid email or password")
        return redirect("/login")

def logout():
    session.clear()

