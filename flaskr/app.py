# app.py

# Import necessary modules from Flask and other libraries
from flask import Flask, redirect, render_template, request, session, url_for, flash, make_response, send_file, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os
import io
import shutil
from datetime import datetime
import csv
import logging
from dotenv import load_dotenv

# Import custom validation functions and database functions
from validation import is_not_empty, is_valid_email, is_within_length, is_secure_password
from db import setup_db, add_user, get_user_id_by_email, get_db_connection
from auth import sign_in, logout

# Load environment variables from .env file
load_dotenv()
# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.getenv('secret_key')  # Secret key for session management
# Configure logging
logging.basicConfig(level=logging.INFO)

#favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Define the home route
@app.route("/")
def home():
    email = "Guest"
    if "email" not in session:
        response = make_response(render_template("home.html", email=email))
    else:
        email = session["email"].split('@')[0]
        response = make_response(render_template("home.html", email=email))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"

    return response

# Define the register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password_confirm = request.form['password_confirm']

        # Validate input fields
        if not all([is_not_empty(email), is_not_empty(password), is_not_empty(first_name), is_not_empty(last_name)]):
            flash("All fields are required", "error")
            return redirect("/register")

        if not is_valid_email(email):
            flash("Invalid email address", "error")
            return redirect("/register")

        if not is_within_length(first_name, 50) or not is_within_length(last_name, 50):
            flash("First name and last name must be 50 characters or less", "error")
            return redirect("/register")

        if password != password_confirm:
            flash("Passwords do not match", "error")
            return redirect("/register")

        if not is_secure_password(password):
            flash("Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.", "error")
            return redirect("/register")

        if not add_user(email, password, first_name, last_name):
            flash("Account already exists", "error")
            return redirect("/register")

        flash("Registration successful!", "success")
        return sign_in(email, password)
    return render_template("register.html")

# Define the login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return sign_in(email, password)

    return render_template("login.html")

# Define the logout route
@app.route("/logout")
def logout_route():
    logout()  
    return redirect(url_for("home"))

# Define the about route
@app.route("/about")
def about():
    return render_template("about.html")

# Define the support route
@app.route("/support", methods=["GET", "POST"])
def support():
    if request.method == "POST":
        subject = request.form["subject"]
        message = request.form["message"]
        
        if "email" in session:
            user_id = get_user_id_by_email(session["email"])
        else:
            user_id = 0  # Use 0 for anonymous users

        conn = get_db_connection()
        cursor = conn.cursor()
        # Insert support message into the database
        cursor.execute(
            "INSERT INTO support (user_id, support) VALUES (?, ?)",
            (user_id, f"{subject}: {message}")
        )
        conn.commit()
        conn.close()

        flash("Your support request has been submitted successfully!", "success")
        return redirect(url_for("support"))

    return render_template("support.html")

# Define the booking route
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'email' not in session:
        flash('Please log in to access the booking page.', 'warning')
        return redirect(url_for('login'))

    user_id = get_user_id_by_email(session['email'])
    if user_id is None:
        flash('User not found.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            participant_id = request.form.get('participant_id')
            
            # Validate participant selection
            if not participant_id:
                flash('Please select a participant or create a new one.', 'warning')
                return redirect(url_for('booking'))
            
            # Handle new participant creation
            if participant_id == 'new':
                name = request.form.get('new_participant_name')
                age = request.form.get('new_participant_age')
                
                # Validate new participant data
                if not name or not age:
                    flash('Please provide both name and age for new participant.', 'warning')
                    return redirect(url_for('booking'))
                
                try:
                    age = int(age)
                    if age < 7 or age > 17:
                        raise ValueError
                except ValueError:
                    flash('Participant age must be between 7 and 17.', 'error')
                    return redirect(url_for('booking'))
                
                # Insert new participant into the database
                cursor.execute(
                    "INSERT INTO participants (user_id, name, age) VALUES (?, ?, ?)",
                    (user_id, name, age)
                )
                participant_id = cursor.lastrowid
            else:
                # Verify participant belongs to user
                cursor.execute(
                    "SELECT COUNT(*) FROM participants WHERE participant_id = ? AND user_id = ?",
                    (participant_id, user_id)
                )
                if cursor.fetchone()[0] == 0:
                    flash('Invalid participant selected.', 'error')
                    return redirect(url_for('booking'))

            # Get activity selections
            activities = []
            for i in range(1, 4):
                activity_id = request.form.get(f'activity{i}')
                if not activity_id:
                    flash(f'Please select activity {i}', 'warning')
                    return redirect(url_for('booking'))
                activities.append(activity_id)
            
            # Verify activities exist
            for activity_id in activities:
                cursor.execute("SELECT COUNT(*) FROM activities WHERE activity_id = ?", (activity_id,))
                if cursor.fetchone()[0] == 0:
                    flash('Invalid activity selected.', 'error')
                    return redirect(url_for('booking'))

            # Get user ID and create the booking
            user_id = get_user_id_by_email(session['email'])
            # Insert new booking into the database
            cursor.execute(
                """INSERT INTO Bookings 
                   (user_id, participant_id, activity1_id, activity2_id, activity3_id) 
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, participant_id, activities[0], activities[1], activities[2])
            )
            booking_id = cursor.lastrowid

            # Handle overflow logic
            cursor.execute("SELECT COUNT(*) FROM Bookings")
            total_bookings = cursor.fetchone()[0]
            overflow_count = 1 if total_bookings > 30 else 0

            cursor.execute(
                "UPDATE Bookings SET overflow_count = ? WHERE booking_id = ?",
                (overflow_count, booking_id)
            )

            conn.commit()
            flash('Booking successfully created!', 'success')
            return redirect(url_for('sessions'))

        except Exception as e:
            conn.rollback()
            flash(f'An error occurred while creating the booking: {str(e)}', 'error')
            return redirect(url_for('booking'))
        
        finally:
            conn.close()

    else:  # GET request
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT participant_id, name FROM participants WHERE user_id = ?",
            (user_id,)
        )
        participants = cursor.fetchall()

        cursor.execute("SELECT activity_id, activity_name FROM activities")
        activities = cursor.fetchall()

        conn.close()
        return render_template('booking.html', participants=participants, activities=activities)

# Define the edit_profile route
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'email' not in session:
        flash('Please log in to edit your profile.', 'warning')
        return redirect(url_for('login'))

    user_id = get_user_id_by_email(session['email'])
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        new_email = request.form['email']
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_password = request.form['password']

        # Hash the new password if provided
        if new_password:
            hashed_password = generate_password_hash(new_password)
            cursor.execute('UPDATE users SET email = ?, first_name = ?, last_name = ?, password = ? WHERE user_id = ?',
                           (new_email, new_first_name, new_last_name, hashed_password, user_id))
        else:
            cursor.execute('UPDATE users SET email = ?, first_name = ?, last_name = ? WHERE user_id = ?',
                           (new_email, new_first_name, new_last_name, user_id))

        conn.commit()
        cursor.execute('SELECT email, first_name, last_name FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        return render_template('edit_profile.html', user_info=user_data)

    # For GET request, fetch the current user data to pre-fill the form
    cursor.execute('SELECT email, first_name, last_name FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    # Fetch participants for the user
    cursor.execute('SELECT participant_id, name, age FROM participants WHERE user_id = ?', (user_id,))
    participants = cursor.fetchall()

    conn.close()

    return render_template('edit_profile.html', user_info=user_data, participant_info=participants)

# Define the sessions route
@app.route('/sessions')
def sessions():
    if 'email' not in session:
        flash('Please log in to access your sessions.', 'warning')
        return redirect(url_for('login'))
    
    user_id = get_user_id_by_email(session['email'])
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch bookings with related participant and activity info
    cursor.execute('''
        SELECT 
            b.booking_id,
            p.name AS participant_name,
            a1.activity_name AS activity1_name,
            a2.activity_name AS activity2_name,
            a3.activity_name AS activity3_name,
            b.overflow_count,
            b.created_at
        FROM bookings b
        JOIN participants p ON b.participant_id = p.participant_id
        LEFT JOIN activities a1 ON b.activity1_id = a1.activity_id
        LEFT JOIN activities a2 ON b.activity2_id = a2.activity_id
        LEFT JOIN activities a3 ON b.activity3_id = a3.activity_id
        WHERE b.user_id = ?
        ORDER BY b.booking_id ASC
    ''', (user_id,))
    
    # Convert tuple results to dictionaries
    bookings = []
    for row in cursor.fetchall():
        booking = {
            'booking_id': row[0],
            'participant_name': row[1],
            'activity1_name': row[2],
            'activity2_name': row[3],
            'activity3_name': row[4],
            'overflow_count': row[5],
            'created_at': row[6]
        }
        bookings.append(booking)
    
    conn.close()
    return render_template('sessions.html', bookings=bookings)

# Define the add_activity route for admin
@app.route('/admin/add_activity', methods=['POST'])
def add_activity():
    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    activity_name = request.form['activity_name']
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert new activity into the database
    cursor.execute('INSERT INTO activities (activity_name) VALUES (?)', (activity_name,))
    conn.commit()
    conn.close()

    flash('Activity added successfully!', 'success')
    return redirect(url_for('admin'))

# Define the admin route
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if "email" not in session:
        flash("Please login to access admin panel", "warning")
        return redirect("/login")
    elif session.get("is_admin"):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch sessions without overflow
        cursor.execute('''
            SELECT 
                b.booking_id,
                p.name AS participant_name,
                a1.activity_name AS activity1_name,
                a2.activity_name AS activity2_name,
                a3.activity_name AS activity3_name,
                b.overflow_count,
                b.created_at
            FROM bookings b
            JOIN participants p ON b.participant_id = p.participant_id
            LEFT JOIN activities a1 ON b.activity1_id = a1.activity_id
            LEFT JOIN activities a2 ON b.activity2_id = a2.activity_id
            LEFT JOIN activities a3 ON b.activity3_id = a3.activity_id
            WHERE b.overflow_count = 0
            ORDER BY b.booking_id ASC
        ''')
        sessions_no_overflow = cursor.fetchall()

        # Fetch sessions with overflow
        cursor.execute('''
            SELECT 
                b.booking_id,
                p.name AS participant_name,
                a1.activity_name AS activity1_name,
                a2.activity_name AS activity2_name,
                a3.activity_name AS activity3_name,
                b.overflow_count,
                b.created_at,
                ROW_NUMBER() OVER (ORDER BY b.overflow_count ASC) AS waiting_list_position
            FROM bookings b
            JOIN participants p ON b.participant_id = p.participant_id
            LEFT JOIN activities a1 ON b.activity1_id = a1.activity_id
            LEFT JOIN activities a2 ON b.activity2_id = a2.activity_id
            LEFT JOIN activities a3 ON b.activity3_id = a3.activity_id
            WHERE b.overflow_count > 0
            ORDER BY b.overflow_count ASC
        ''')
        sessions_with_overflow = cursor.fetchall()

        # Fetch support messages
        cursor.execute('SELECT * FROM support ORDER BY created_at DESC')
        support_messages = cursor.fetchall()

        # Fetch activities
        cursor.execute('SELECT * FROM activities ORDER BY activity_name ASC')
        activities = cursor.fetchall()

        conn.close()
        return render_template('admin.html', sessions_no_overflow=sessions_no_overflow, sessions_with_overflow=sessions_with_overflow, support_messages=support_messages, activities=activities)
    else:
        flash("Access denied: Admin privileges required", "error")
        return redirect("/")

# Define the delete_activity route for admin
@app.route('/admin/delete_activity/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete activity from the database
    cursor.execute('DELETE FROM activities WHERE activity_id = ?', (activity_id,))
    conn.commit()
    conn.close()

    flash('Activity deleted successfully!', 'success')
    return redirect(url_for('admin'))

# Define the edit_session route for admin
@app.route('/admin/edit_session/<int:booking_id>', methods=['GET', 'POST'])
def edit_session(booking_id):
    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        participant_id = request.form.get('participant_id')
        activity1_id = request.form.get('activity1_id')
        activity2_id = request.form.get('activity2_id')
        activity3_id = request.form.get('activity3_id')

        # Update session details in the database
        cursor.execute('''
            UPDATE bookings
            SET participant_id = ?, activity1_id = ?, activity2_id = ?, activity3_id = ?
            WHERE booking_id = ?
        ''', (participant_id, activity1_id, activity2_id, activity3_id, booking_id))
        conn.commit()
        flash('Session updated successfully!', 'success')
        return redirect(url_for('admin'))

    cursor.execute('''
        SELECT 
            b.booking_id,
            p.name AS participant_name,
            a1.activity_name AS activity1_name,
            a2.activity_name AS activity2_name,
            a3.activity_name AS activity3_name,
            b.overflow_count,
            b.created_at
        FROM bookings b
        JOIN participants p ON b.participant_id = p.participant_id
        LEFT JOIN activities a1 ON b.activity1_id = a1.activity_id
        LEFT JOIN activities a2 ON b.activity2_id = a2.activity_id
        LEFT JOIN activities a3 ON b.activity3_id = a3.activity_id
        WHERE b.booking_id = ?
    ''', (booking_id,))
    session_data = cursor.fetchone()

    cursor.execute('SELECT participant_id, name FROM participants')
    participants = cursor.fetchall()

    cursor.execute('SELECT activity_id, activity_name FROM activities')
    activities = cursor.fetchall()

    conn.close()
    return render_template('edit_session.html', session_data=session_data, participants=participants, activities=activities)

# Define the delete_session route
@app.route('/admin/delete_session/<int:booking_id>', methods=['POST'])
def delete_session(booking_id):
    if 'email' not in session:
        flash('Please log in to delete a session.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user is an admin
    if session.get('is_admin'):
        cursor.execute('DELETE FROM bookings WHERE booking_id = ?', (booking_id,))
    else:
        # Verify that the session belongs to the logged-in user
        user_id = get_user_id_by_email(session['email'])
        cursor.execute('SELECT COUNT(*) FROM bookings WHERE booking_id = ? AND user_id = ?', (booking_id, user_id))
        if cursor.fetchone()[0] == 0:
            flash('Invalid session selected.', 'error')
            return redirect(url_for('sessions'))

        cursor.execute('DELETE FROM bookings WHERE booking_id = ?', (booking_id,))

    conn.commit()

    # Move the lowest overflow session to the main list
    cursor.execute('''
        SELECT booking_id FROM bookings WHERE overflow_count > 0 ORDER BY overflow_count ASC LIMIT 1
    ''')
    lowest_overflow_session = cursor.fetchone()
    if lowest_overflow_session:
        cursor.execute('''
            UPDATE bookings SET overflow_count = 0 WHERE booking_id = ?
        ''', (lowest_overflow_session[0],))
        conn.commit()

    conn.close()
    flash('Session deleted successfully!', 'success')
    return redirect(url_for('admin' if session.get('is_admin') else 'sessions'))

# Define the delete_support route for admin
@app.route('/admin/delete_support/<int:support_id>', methods=['POST'])
def delete_support(support_id):
    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete support message from the database
    cursor.execute('DELETE FROM support WHERE support_id = ?', (support_id,))
    conn.commit()
    conn.close()

    flash('Support message deleted successfully!', 'success')
    return redirect(url_for('admin'))

# Define the backup_database route for admin
@app.route('/admin/backup_database', methods=['POST'])
def backup_database():
    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    backup_folder = 'backup'
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = os.path.join(backup_folder, f'dojo_backup_{timestamp}.db')

    try:
        shutil.copy('dojo.db', backup_file)
        flash('Database backup created successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred while creating the backup: {str(e)}', 'error')

    return redirect(url_for('admin'))

# Define the download_data route
@app.route('/download_data')
def download_data():
    if 'email' not in session:
        flash('Please log in to download your data.', 'warning')
        return redirect(url_for('login'))

    user_id = get_user_id_by_email(session['email'])
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user data
    cursor.execute('SELECT email, first_name, last_name FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    # Fetch participant data
    cursor.execute('SELECT name, age FROM participants WHERE user_id = ?', (user_id,))
    participants = cursor.fetchall()

    conn.close()

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Email', 'First Name', 'Last Name'])
    writer.writerow(user_data)
    writer.writerow([])
    writer.writerow(['Participants'])
    writer.writerow(['Name', 'Age'])
    for participant in participants:
        writer.writerow(participant)

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='user_data.csv'
    )

# Define the add_participant route
@app.route('/add_participant', methods=['POST'])
def add_participant():
    if 'email' not in session:
        flash('Please log in to add a participant.', 'warning')
        return redirect(url_for('login'))

    user_id = get_user_id_by_email(session['email'])
    name = request.form['new_participant_name']
    age = request.form['new_participant_age']

    if not name or not age:
        flash('Please provide both name and age for the new participant.', 'warning')
        return redirect(url_for('edit_profile'))

    try:
        age = int(age)
        if age < 7 or age > 17:
            raise ValueError
    except ValueError:
        flash('Participant age must be between 7 and 17.', 'error')
        return redirect(url_for('edit_profile'))

    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert new participant into the database
    cursor.execute(
        "INSERT INTO participants (user_id, name, age) VALUES (?, ?, ?)",
        (user_id, name, age)
    )
    conn.commit()
    conn.close()

    flash('Participant added successfully!', 'success')
    return redirect(url_for('edit_profile'))

# Define the delete_account route
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'email' not in session:
        flash('Please log in to delete your account.', 'warning')
        return redirect(url_for('login'))

    user_id = get_user_id_by_email(session['email'])
    password = request.form['delete_password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user and check_password_hash(user[0], password):
        # Delete user-related data
        cursor.execute('DELETE FROM bookings WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM participants WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM support WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

        session.clear()
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('home'))
    else:
        flash('Incorrect password. Please try again.', 'error')
        return redirect(url_for('edit_profile'))

# Define error handlers for various HTTP status codes
@app.errorhandler(404)
def page_not_found(e):
    logging.info(f"404 error: {request.url}")
    flash('Page not found', 'error')
    return redirect(url_for('home'))  

@app.errorhandler(500)
def internal_server_error(e):
    flash('Internal server error', 'error')
    return redirect("/")

@app.errorhandler(405)
def method_not_allowed(e):
    flash('Method not allowed', 'error')
    return redirect("/")

@app.errorhandler(403)
def forbidden(e):
    flash('Access denied', 'error')
    return redirect("/")

@app.errorhandler(401)
def unauthorized(e):
    flash('Unauthorized access', 'error')
    return redirect("/")

@app.errorhandler(400)
def bad_request(e):
    flash('Bad request', 'error')
    return redirect("/")

@app.errorhandler(413)
def request_entity_too_large(e):
    flash('Request entity too large', 'error')
    return redirect("/")

# Define the status route for admin
@app.route('/status', methods=['POST'])
def status():
    messages = []

    # get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # check if all required files are present
    required_files = ['app.py', 'auth.py', 'db.py', 'validation.py', 'templates/base.html']
    for file in required_files:
        file_path = os.path.join(current_dir, file)
        if not os.path.exists(file_path):
            messages.append(f"missing required file: {file}")

    # check database connection
    try:
        conn = get_db_connection()
        conn.execute('select 1')
        conn.close()
        messages.append("database connection: ok")
    except Exception as e:
        messages.append(f"database connection error: {str(e)}")

    if not messages:
        messages.append("all checks passed successfully!")

    for message in messages:
        flash(message, 'info')

    return redirect(url_for('admin'))

# Define the set_cookie route
@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('cookie_consent', 'true', max_age=60*60*24*365)  # 1 year
    return response

# Define the download route
@app.route('/download')
def download():
    return send_file(
        'path/to/your/file',
        download_name='your_file_name.ext',
        as_attachment=True
    )

# Main entry point of the application
if __name__ == '__main__':
    setup_db()
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        from gunicorn.app.wsgiapp import run
        run()