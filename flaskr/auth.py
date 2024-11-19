# auth.py
from flask import session, flash, redirect
from db import get_db_connection

def sign_in(email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """SELECT Email, is_admin FROM Users WHERE Email = ? AND Password = ?"""
    cur.execute(query, (email, password))
    user = cur.fetchone()
    conn.close()

    if user:
        session["email"] = user[0]  # Email
        session["is_admin"] = bool(user[1])  # is_admin
        if session["is_admin"]:
            return redirect("/admin")
        return redirect("/")
    else:
        flash("Invalid email or password")
        return redirect("/login")

def logout():
    session.clear()