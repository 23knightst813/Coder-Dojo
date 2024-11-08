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
    
    # Split queries into individual statements
    statements = [
        # Drop participants table if it exists
        """DROP TABLE IF EXISTS participants""",
        # Create bookings table
        """CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name VARCHAR(100) NOT NULL,
            age INT NOT NULL CHECK (age BETWEEN 5 AND 16),
            activity_1 VARCHAR(100) NOT NULL,
            activity_2 VARCHAR(100) NOT NULL,
            activity_3 VARCHAR(100) NOT NULL,
            booking_date DATE NOT NULL DEFAULT CURRENT_DATE,
            booking_time TIME NOT NULL DEFAULT CURRENT_TIME,
            overflow INT NOT NULL DEFAULT 0
        )""",
        # Create Users table
        """CREATE TABLE IF NOT EXISTS Users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            First_Name TEXT,
            Last_Name TEXT,
            Creation_Date DATETIME DEFAULT CURRENT_TIMESTAMP
        )""",
        # Create activities table
        """CREATE TABLE IF NOT EXISTS activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_name VARCHAR(100) NOT NULL,
            description TEXT
        )""",
        # Insert activities data
        """INSERT OR IGNORE INTO activities (activity_name, description) VALUES
            ('Scratch', 'Learn to code animations, stories, and games')""",
        """INSERT OR IGNORE INTO activities (activity_name, description) VALUES
            ('Unity', 'Create and explore 3D worlds')""",
        """INSERT OR IGNORE INTO activities (activity_name, description) VALUES
            ('Web Design', 'Build websites and apps with HTML, CSS, and JavaScript')""",
        # Create participants table
        """CREATE TABLE participants (
            participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name VARCHAR(50) NOT NULL,
            age INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(userID)
        )""",
        # Insert test data into participants table
        """INSERT INTO participants (user_id, name, age) VALUES
            (1, 'John Doe', 25)"""
    ]
    
    # Execute each statement individually
    for statement in statements:
        cur.execute(statement)
    
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
