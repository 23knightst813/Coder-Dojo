# app.py
from flask import Flask, redirect, render_template, request, session, url_for, flash, make_response
from werkzeug.security import generate_password_hash
import os
import shutil
from datetime import datetime

from validation import is_not_empty, is_valid_email, is_within_length, is_secure_password
from db import setup_db, add_user, get_user_id_by_email, get_db_connection
from auth import sign_in, logout

app = Flask(__name__)
app.secret_key = 'RaheeshSucks'

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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password_confirm = request.form['password_confirm']

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return sign_in(email, password)

    return render_template("login.html")

@app.route("/logout")
def logout_route():
    logout()  
    return redirect(url_for("home"))

@app.route("/about")
def about():
    return render_template("about.html")

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
        cursor.execute(
            "INSERT INTO support (user_id, support) VALUES (?, ?)",
            (user_id, f"{subject}: {message}")
        )
        conn.commit()
        conn.close()

        flash("Your support request has been submitted successfully!", "success")
        return redirect(url_for("support"))

    return render_template("support.html")

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
                    if age <= 0:
                        raise ValueError
                except ValueError:
                    flash('Please provide a valid age.', 'error')
                    return redirect(url_for('booking'))
                
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

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'email' not in session:
        flash('Please log in to access the profile page.', 'warning')
        return redirect(url_for('login'))

    user_email = session['email']
    user_id = get_user_id_by_email(user_email)
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Update user information
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        cursor.execute('''
            UPDATE users SET first_name = ?, last_name = ?, password = ? WHERE user_id = ?
        ''', (first_name, last_name, hashed_password, user_id))

        # Update existing participants
        participant_ids = request.form.getlist('participant_id')
        participant_names = request.form.getlist('participant_name')
        participant_ages = request.form.getlist('participant_age')

        for p_id, p_name, p_age in zip(participant_ids, participant_names, participant_ages):
            cursor.execute('''
                UPDATE participants SET name = ?, age = ? WHERE participant_id = ? AND user_id = ?
            ''', (p_name, p_age, p_id, user_id))

        # Add new participants
        new_participant_names = request.form.getlist('new_participant_name')
        new_participant_ages = request.form.getlist('new_participant_age')

        for name, age in zip(new_participant_names, new_participant_ages):
            if name.strip() and age.strip():
                cursor.execute('''
                    INSERT INTO participants (user_id, name, age) VALUES (?, ?, ?)
                ''', (user_id, name, age))

        conn.commit()
        conn.close()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('edit_profile'))

    else:
        # Retrieve user information
        cursor.execute('SELECT first_name, last_name, password FROM users WHERE user_id = ?', (user_id,))
        user_info = cursor.fetchone()

        # Retrieve participant information
        cursor.execute('SELECT participant_id, name, age FROM participants WHERE user_id = ?', (user_id,))
        participant_info = cursor.fetchall()

        conn.close()
        return render_template('edit_profile.html', user_info=user_info, participant_info=participant_info)

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


@app.route("/admin")
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

        conn.close()
        return render_template('admin.html', sessions_no_overflow=sessions_no_overflow, sessions_with_overflow=sessions_with_overflow, support_messages=support_messages)
    else:
        flash("Access denied: Admin privileges required", "error")
        return redirect("/")

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

@app.route('/admin/delete_session/<int:booking_id>', methods=['POST'])
def delete_session(booking_id):
    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

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
    return redirect(url_for('admin'))

@app.route('/admin/delete_support/<int:support_id>', methods=['POST'])
def delete_support(support_id):
    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM support WHERE support_id = ?', (support_id,))
    conn.commit()
    conn.close()

    flash('Support message deleted successfully!', 'success')
    return redirect(url_for('admin'))

    if 'email' not in session or not session.get('is_admin'):
        flash('Access denied: Admin privileges required', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET email = ?, password = ?, first_name = ?, last_name = ?
            WHERE email = ?
        ''', (email, password, first_name, last_name, session['email']))
        conn.commit()
        conn.close()

        session['email'] = email
        flash('Account updated successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('edit_account.html')

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

@app.errorhandler(404)
def page_not_found(e):
    flash('Page not found', 'error')
    return redirect("/")    


@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('cookie_consent', 'true', max_age=60*60*24*365)  # 1 year
    return response

if __name__ == '__main__':
    setup_db()
    app.run(debug=True)