# db.py
import sqlite3
import datetime

def get_db_connection():
    conn = sqlite3.connect('Bean_N_Data.db')
    print("Connection to database established, connection object is: ", conn)
    return conn


def get_user_id_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT userID FROM Users WHERE Email = ?", (email,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def setup_db():
    print("Setting up database")
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Split queries into individual statements
    statements = [
        # Create bookings table
        """
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            activity1_id INTEGER,
            activity2_id INTEGER,
            activity3_id INTEGER,
            overflow_count INTEGER DEFAULT 0,
            FOREIGN KEY (participant_id) REFERENCES participants(participant_id),
            FOREIGN KEY (activity1_id) REFERENCES activities(activity_id),
            FOREIGN KEY (activity2_id) REFERENCES activities(activity_id),
            FOREIGN KEY (activity3_id) REFERENCES activities(activity_id)
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
        """CREATE TABLE IF NOT EXISTS participants (
            participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name VARCHAR(50) NOT NULL,
            age INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(userID)
        )""",
        # Insert test data into participants table
        """INSERT OR IGNORE INTO participants (user_id, name, age) VALUES
            (1, 'John Doe', 25)"""
    ]
    
    try:
        # Execute each statement individually
        for statement in statements:
            cur.execute(statement)
        conn.commit()
    finally:
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
