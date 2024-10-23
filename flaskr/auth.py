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
