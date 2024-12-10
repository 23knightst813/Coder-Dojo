# db.py
# Purpose: Handles database setup and operations for the Coder Dojo web application
# Author: Theo
# Date: 28 November 2024
# Notes: Implements database schema creation and user management functions.

# Import the sqlite3 module for database operations
import sqlite3
# Import the generate_password_hash function from werkzeug.security for password hashing
from werkzeug.security import generate_password_hash

# Function to set up the database by creating necessary tables and adding an admin account
def setup_db():
    """
    Set up the database by creating necessary tables and adding an admin account.

    Returns:
        None
    """
    # Connect to the SQLite database 'dojo.db'
    conn = sqlite3.connect('dojo.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    
    # Create the 'users' table if it doesn't exist
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
    
    # Create the 'participants' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create the 'activities' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_name TEXT NOT NULL
        )
    ''')
    
    # Create the 'Bookings' table if it doesn't exist
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
    
    # Create the 'support' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support (
            support_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            support TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    # Add an admin account if it doesn't exist
    admin_email = 'admin@codeclub.com'
    admin_password = generate_password_hash('adminpass')
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password, first_name, last_name, is_admin)
        VALUES (?, ?, 'Admin', 'User', TRUE)
    ''', (admin_email, admin_password))

    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()

# Function to add a new user to the database
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
    # Connect to the SQLite database 'dojo.db'
    conn = sqlite3.connect('dojo.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # Hash the plain-text password
    hashed_password = generate_password_hash(password)
    try:
        # Insert the new user into the 'users' table
        cursor.execute('''
            INSERT INTO users (email, password, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (email, hashed_password, first_name, last_name))
        # Commit the changes to the database
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        # Close the database connection
        conn.close()

# Function to get the user ID based on the provided email
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
    # Connect to the SQLite database 'dojo.db'
    conn = sqlite3.connect('dojo.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # Execute a query to fetch the user ID based on the provided email
    cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
    # Fetch the result from the query
    result = cursor.fetchone()
    # Close the database connection
    conn.close()
    # Return the user ID if found, otherwise return None
    return result[0] if result else None

# Function to get a connection to the database
def get_db_connection():
    """
    Get a connection to the database.

    Returns:
        Connection: A SQLite database connection.

    Raises:
        None
    """
    # Return a connection to the SQLite database 'dojo.db'
    return sqlite3.connect('dojo.db')