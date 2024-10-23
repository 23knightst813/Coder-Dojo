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
        return redirect("/")

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

@app.route("/login", methods=["GET", "POST"])
def login():
    print("Login start")
    if request.method == "POST":
        print("Post")
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]

        if sign_in(EMAIL, PASSWORD):
            session["email"] = EMAIL
            print("Logged in")
            return redirect("/")
        else:
            flash("Invalid email or password")
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout_route():
    logout()  
    return redirect(url_for("home"))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

if __name__ == '__main__':
    setup_db()
    app.run(debug=True)
