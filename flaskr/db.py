# db.py
# Purpose: Handles database setup and operations for the Coder Dojo web application
# Author: Theo
# Date: 28 November 2024
# Notes: Implements database schema creation and user management functions.

import sqlite3
from werkzeug.security import generate_password_hash

def setup_db():
    """
    Set up the database by creating necessary tables.

    Returns:
        None
    """
    conn = sqlite3.connect('dojo.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Create participants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_name TEXT NOT NULL
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            participant_id INTEGER NOT NULL,
            activity1_id INTEGER,
            activity2_id INTEGER,
            activity3_id INTEGER,
            overflow_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (participant_id) REFERENCES participants(participant_id),
            FOREIGN KEY (activity1_id) REFERENCES activities(activity_id),
            FOREIGN KEY (activity2_id) REFERENCES activities(activity_id),
            FOREIGN KEY (activity3_id) REFERENCES activities(activity_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support (
            support_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            support TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(email, password, first_name, last_name):
    """
    Add a new user to the database.

    Parameters:
        email (str): The email of the user.
        password (str): The plain-text password provided by the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.

    Returns:
        bool: True if the user is added successfully, False otherwise.

    Raises:
        None
    """
    conn = sqlite3.connect('dojo.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute('''
            INSERT INTO users (email, password, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (email, hashed_password, first_name, last_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_id_by_email(email):
    """
    Get the user ID based on the provided email.

    Parameters:
        email (str): The email of the user.

    Returns:
        int: The user ID if found, None otherwise.

    Raises:
        None
    """
    conn = sqlite3.connect('dojo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_db_connection():
    """
    Get a connection to the database.

    Returns:
        Connection: A SQLite database connection.

    Raises:
        None
    """
    return sqlite3.connect('dojo.db')
