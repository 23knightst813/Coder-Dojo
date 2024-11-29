# auth.py
# Purpose: Handles user authentication, including sign-in and logout functionality
# Author: Theo
# Date: 28 November 2024
# Notes: Implements password hashing for secure authentication.

# Import necessary modules from Flask and other libraries
from flask import session, flash, redirect
from db import get_db_connection
from werkzeug.security import check_password_hash

# Function to authenticate a user by validating their credentials
def sign_in(email, password):
    """
    Authenticate a user by validating their credentials.

    Parameters:
        email (str): The email of the user.
        password (str): The plain-text password provided by the user.

    Returns:
        Response: Redirect to the appropriate page based on the authentication outcome.

    Raises:
        None
    """
    conn = get_db_connection()  # Get a connection to the database
    cur = conn.cursor()  # Create a cursor object to interact with the database
    query = """SELECT email, password, is_admin FROM users WHERE email = ?"""
    cur.execute(query, (email,))  # Execute the query to fetch user data based on the provided email
    user = cur.fetchone()  # Fetch the first result from the query
    conn.close()  # Close the database connection

    if user and check_password_hash(user[1], password):  # Check if user exists and password is correct
        session["email"] = user[0]  # Store the user's email in the session
        session["is_admin"] = bool(user[2])  # Store the user's admin status in the session
        if session["is_admin"]:  # If the user is an admin, redirect to the admin page
            return redirect("/admin")
        return redirect("/")  # Otherwise, redirect to the home page
    else:
        flash("Invalid email or password")  # Display an error message if authentication fails
        return redirect("/login")  # Redirect to the login page

# Function to clear the user session to log out the user
def logout():
    """
    Clear the user session to log out the user.

    Returns:
        None
    """
    session.clear()  # Clear all data from the session
