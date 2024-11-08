# app.py
from flask import Flask, redirect, render_template, request, session, url_for, make_response, flash
from db import setup_db, add_user
from auth import sign_in, logout

app = Flask(__name__)
app.secret_key = 'RaheeshSucks'

@app.route("/register", methods=["GET", "POST"])
def register():
    print("Register start")
    if request.method == "POST":
        print("Post")
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            flash("Passwords do not match")
            print("Passwords do not match")
            return redirect("/register")

        if not add_user(email, password, first_name, last_name):
            flash("Account already exists")
            return redirect("/register")

        # Create a session for the user
        session['email'] = email
        if sign_in(email, password):
            session["email"] = email
            if email == "theo@theo.com":
                session["is_admin"] = True  
                print("Logged in as Admin")
                redirect("/admin")
            else:
                session["is_admin"] = False
                print("Logged in as Regular User")
                return redirect("/")
        else:
            flash("Invalid email or password")
            return redirect("/login")

    return render_template('register.html')

@app.route("/")
def home():
    email = "Guest"
    print("Home start")
    
    if "email" not in session:
        print("No email in session")
        print('Sign In as Guest')
        response = make_response(render_template("home.html", email=email))
    else:
        email = session["email"].split('@')[0]
        response = make_response(render_template("home.html", email=email))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"

    return response



@app.route("/admin")
def admin_route():
    # Check if user is logged in
    if "email" not in session:
        flash("Please login first")
        return redirect("/login")
    
    # Check admin status with get() to avoid KeyError
    is_admin = session.get("is_admin", False)
    
    if is_admin:
        return render_template("admin.html")
    else:
        flash("Access denied: Admin privileges required")
        return redirect("/")

# app.py
@app.route("/login", methods=["GET", "POST"])
def login():
    print("Login start")
    if request.method == "POST":
        print("Post")
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]

        if sign_in(EMAIL, PASSWORD):
            session["email"] = EMAIL
            if EMAIL == "theo@theo.com":
                session["is_admin"] = True  
                print("Logged in as Admin")
                redirect("/admin")
            else:
                session["is_admin"] = False
                print("Logged in as Regular User")
            return redirect("/")
        else:
            flash("Invalid email or password")
            return redirect("/login")

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
    elif session["email"] == "Admin":
        return render_template("admin.html")
    return redirect("/")

@app.route("/booking")
def booking():
    return render_template("booking.html")


if __name__ == '__main__':
    setup_db()
    app.run(debug=True)
