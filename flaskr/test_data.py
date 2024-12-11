# test_data.py
# Purpose: Populate the database with test data for sessions to test overflow functionality
# Author: Theo
# Date: 28 November 2024

from werkzeug.security import generate_password_hash
import sqlite3

def populate_test_data():
    """
    Populate the database with test data for sessions to test overflow functionality.

    Returns:
        None
    """
    # Connect to the SQLite database 'dojo.db'
    conn = sqlite3.connect('dojo.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Insert test data into the 'activities' table
    activities = [
        ('Coding 101',),
        ('Robotics',),
        ('Game Development',)
    ]
    cursor.executemany('INSERT INTO activities (activity_name) VALUES (?)', activities)

    # Insert test data into the 'users' table
    users = [
        ('user1@example.com', 'password1', 'User', 'One'),
        ('user2@example.com', 'password2', 'User', 'Two'),
        ('user3@example.com', 'password3', 'User', 'Three')
    ]
    for email, password, first_name, last_name in users:
        cursor.execute('INSERT INTO users (email, password, first_name, last_name) VALUES (?, ?, ?, ?)',
                       (email, generate_password_hash(password), first_name, last_name))

    # Insert test data into the 'participants' table
    participants = [
        (1, 'Participant One', 10),
        (2, 'Participant Two', 12),
        (3, 'Participant Three', 11)
    ]
    cursor.executemany('INSERT INTO participants (user_id, name, age) VALUES (?, ?, ?)', participants)

    # Insert test data into the 'Bookings' table to test overflow
    bookings = [
        (1, 1, 1, 2, 3, 1),
        (2, 2, 1, 2, 3, 1),
        (3, 3, 1, 2, 3, 1)
    ]
    cursor.executemany('''
        INSERT INTO Bookings (user_id, participant_id, activity1_id, activity2_id, activity3_id, overflow_count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', bookings)

    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    print('Test data populated successfully.')
if __name__ == '__main__':
    populate_test_data()