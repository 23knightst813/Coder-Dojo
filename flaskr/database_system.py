import sqlite3


# Function to set up database
def setup_db():

    print("Setting up database")
    conn = get_db_connection()
    cur = conn.cursor()
    #User table
    query = """CREATE TABLE IF NOT EXISTS Users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        First_Name TEXT,
        Last_Name TEXT,
        Creation_Date DATETIME DEFAULT CURRENT_TIMESTAMP
    )"""

    cur.execute(query)
    print("Created Users table")
    conn.commit()
    conn.close()



# Function to establish connection to the database
def get_db_connection():

    conn = sqlite3.connect('Dojo.db')
    print("Connection to database established , connection object is: ", conn)
    return conn
