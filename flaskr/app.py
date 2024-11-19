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
            flash("Passwords do not match")
            return redirect("/register")

        if not add_user(email, password, first_name, last_name):
            flash("Account already exists")
            return redirect("/register")

        return sign_in(email, password)

    return render_template('register.html')

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
        return redirect("/login")
    elif session.get("is_admin"):
        return render_template("admin.html")
    flash("Access denied: Admin privileges required")
    return redirect("/")

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'email' not in session:
        flash('Please log in to access the booking page.')
        return redirect(url_for('login'))

    user_id = get_user_id_by_email(session['email'])
    if user_id is None:
        flash('User not found.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        participant_id = request.form.get('participant_id')
        if participant_id == 'new':
            name = request.form.get('new_participant_name')
            age = request.form.get('new_participant_age')
            cursor.execute(
                "INSERT INTO participants (user_id, name, age) VALUES (?, ?, ?)",
                (user_id, name, age)
            )
            participant_id = cursor.lastrowid
        else:
            participant_id = int(participant_id)

        activity_ids = []
        for i in range(1, 4):
            activity_id = request.form.get(f'activity{i}')
            if activity_id:
                activity_ids.append(activity_id)
            else:
                activity_ids.append(None)

        cursor.execute(
            "INSERT INTO Bookings (participant_id, activity1_id, activity2_id, activity3_id) VALUES (?, ?, ?, ?)",
            (
                participant_id,
                activity_ids[0],
                activity_ids[1],
                activity_ids[2],
            )
        )
        booking_id = cursor.lastrowid

        cursor.execute("SELECT COUNT(*) FROM Bookings")
        total_bookings = cursor.fetchone()[0]
        overflow_count = 1 if total_bookings > 30 else 0

        cursor.execute(
            "UPDATE Bookings SET overflow_count = ? WHERE booking_id = ?",
            (overflow_count, booking_id)
        )

        conn.commit()
        conn.close()
        flash('Booking successfully created.')
        return redirect(url_for('home'))

    else:
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
