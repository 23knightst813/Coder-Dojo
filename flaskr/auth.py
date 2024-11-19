# auth.py
from flask import session, flash
from db import get_db_connection

def sign_in(email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """SELECT * FROM Users WHERE Email = ? AND Password = ?"""
    cur.execute(query, (email, password))
    user = cur.fetchone()
    conn.close()

    return user is not None  # Return True if user exists

def logout():
    session.clear()

def admin_sign_in(email, password):
    if sign_in(email, password):
        session["email"] = email
        if email == "theo@theo.com" or email == "a@a.co.fortei":
            session["is_admin"] = True  
            return redirect("/admin")
        else:
            session["is_admin"] = False
            return redirect("/")
    else:
        flash("Invalid email or password")
        return redirect("/login")