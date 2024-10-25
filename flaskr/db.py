# db.py
import sqlite3
import datetime

def get_db_connection():
    conn = sqlite3.connect('Bean_N_Data.db')
    print("Connection to database established, connection object is: ", conn)
    return conn

def setup_db():
    print("Setting up database")
    conn = get_db_connection()
    cur = conn.cursor()
    queries = [
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name VARCHAR(100) NOT NULL,
            age INT NOT NULL CHECK (age BETWEEN 5 AND 16),
            activity_1 VARCHAR(100) NOT NULL,
            activity_2 VARCHAR(100) NOT NULL,
            activity_3 VARCHAR(100) NOT NULL,
            booking_date DATE NOT NULL DEFAULT CURRENT_DATE,
            booking_time TIME NOT NULL DEFAULT CURRENT_TIME,
            overflow INT NOT NULL DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            First_Name TEXT,
            Last_Name TEXT,
            Creation_Date DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]

    # Execute each query individually
    for query in queries:
        cur.execute(query)
    conn.commit()
    conn.close()

def add_user(email, password, first_name, last_name):
    Creation_Date = datetime.datetime.now()
    conn = get_db_connection()
    cur = conn.cursor()
    query = """INSERT INTO Users (Email, Password, First_Name, Last_Name, Creation_Date)
               VALUES (?, ?, ?, ?, ?)"""
    try:
        cur.execute(query, (email, password, first_name, last_name, Creation_Date))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # User already exists
    finally:
        conn.close()

    return True
