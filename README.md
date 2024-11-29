# Coder Dojo Web Application  

This web application is designed for a coding club to manage user registrations, bookings, and support messages. It provides a seamless experience for users to register, log in, book activities, manage their profiles, and seek support. Admin users have additional privileges to manage sessions and view support messages.  

---

## Instructions to Run the Program  

### Clone the Repository  
```bash
git clone https://github.com/23knightst813/Coder-Dojo.git
cd flasky
```  

### Create a Virtual Environment  
```bash
python -m venv venv
```  

### Activate the Virtual Environment  
#### On Windows:  
```bash
venv\Scripts\activate
```  
#### On macOS/Linux:  
```bash
source venv/bin/activate
```  

### Install the Dependencies  
```bash
pip install -r requirements.txt
```  

### Set Up the Database  
Run the database setup script:  
```bash
python db.py
```  

### Run the Application  
```bash
flask run
```  

### Access the Application  
Open your web browser and go to:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)  

---

## Dependencies and System Requirements  

### Python Packages  
- **Flask**: A micro web framework for Python.  
- **sqlite3**: A lightweight, disk-based database library.  

---

## Project Structure  
```
flaskr/  
├── app.py            # Main application file  
├── auth.py           # Authentication-related functions  
├── db.py             # Database connection and utility functions  
├── static/           # Static files (e.g., CSS)  
└── templates/        # HTML templates  
```  

---

## Known Limitations and Areas for Improvement  

### Scalability  
- **Limitation**: The application uses SQLite, suitable for small-scale applications but not for handling high traffic or large datasets.  
- **Improvement**: Consider migrating to a more robust database system like PostgreSQL or MySQL for better scalability and performance.  

### User Authentication  
- **Limitation**: Lacks advanced security features such as multi-factor authentication (MFA) and account lockout mechanisms.  
- **Improvement**: Implement additional security measures to protect against brute force attacks.  

### Database Handling  
- **Limitation**: Database connection and cursor creation are repeated across multiple functions.  
- **Improvement**: Centralise database handling to reduce redundancy.  

### Error Handling  
- **Limitation**:  
  - `add_user` function only catches `sqlite3.IntegrityError`.  
  - `sign_in` function does not handle database connection failures.  
- **Improvement**: Improve error handling to cover edge cases.  

### Security  
- **Limitation**:  
  - The secret key is hardcoded in `app.py`.  
  - Passwords are stored in plain text.  
- **Improvement**:  
  - Move the secret key to an environment variable.  
  - Implement a secure hashing algorithm (e.g., bcrypt) for storing passwords.  

### Input Validation  
- **Limitation**: Input validation during user registration and support message submission is limited.  
- **Improvement**: Add stricter validation for user inputs to prevent invalid data entry.  

---

## Notable Changes and Their Rationale

### Addition of User Authentication

**What was changed:**
- Implemented user authentication using email and password.
- Added password hashing for secure authentication.

**Why the change was necessary:**
- To ensure that only authorized users can access certain features of the application.
- To enhance security by protecting user passwords.

**Supporting Evidence:**
- Password hashing is a standard practice in the industry to protect user credentials.
- References: [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

### Implementation of Booking System

**What was changed:**
- Added functionality for users to book activities.
- Implemented validation for participant selection and activity choices.

**Why the change was necessary:**
- To allow users to book activities and manage their bookings.
- To ensure that the booking process is user-friendly and error-free.

**Supporting Evidence:**
- User feedback indicated a need for a streamlined booking process.
- References: [Usability.gov - Booking Systems](https://www.usability.gov/what-and-why/booking-systems.html)

### Enhancement of Admin Panel

**What was changed:**
- Added features for admin users to manage sessions and view support messages.
- Implemented functionality to add and delete activities.

**Why the change was necessary:**
- To provide admin users with the tools to manage the application effectively.
- To ensure that the admin panel is comprehensive and user-friendly.

**Supporting Evidence:**
- Admin feedback indicated a need for more control over the application.
- References: [Nielsen Norman Group - Admin Interfaces](https://www.nngroup.com/articles/admin-interfaces/)

For more detailed information, please refer to the [Change Rationale Document](documentation/change_rationale.md).
