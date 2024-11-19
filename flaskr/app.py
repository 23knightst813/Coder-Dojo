# app.py
from flask import Flask, redirect, render_template, request, session, url_for, flash, make_response
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

        if password != password_confirm:
            flash("Passwords do not match", "error")
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

@app.route("/admin")
def admin():
    if "email" not in session:
        flash("Please login to access admin panel", "warning")
        return redirect("/login")
    elif session.get("is_admin"):
        flash("Welcome to admin panel", "success")
        return render_template("admin.html")
    flash("Access denied: Admin privileges required", "error")
    return redirect("/")

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

            # Create the booking
            cursor.execute(
                """INSERT INTO Bookings 
                   (participant_id, activity1_id, activity2_id, activity3_id) 
                   VALUES (?, ?, ?, ?)""",
                (participant_id, activities[0], activities[1], activities[2])
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
            return redirect(url_for('home'))

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


if __name__ == '__main__':
    setup_db()
    app.run(debug=True)
