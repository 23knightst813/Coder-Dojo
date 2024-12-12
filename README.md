# Coder Dojo Web Application  

This web application is designed for a coding club to manage user registrations, bookings, and support messages. It provides a seamless experience for users to register, log in, book activities, manage their profiles, and seek support. Admin users have additional privileges to manage sessions and view support messages.  

---

## Instructions to Run the Program  

### Clone the Repository  
```bash
git clone https://github.com/23knightst813/Coder-Dojo.git
```  
### Enter the directory
```  
cd flaskyy
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

### Run the Application  
```bash
python app.py
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
- **Improvement**:  
  - Move the secret key to an environment variable.  

### Input Validation  
- **Limitation**: Input validation during user registration and support message submission is limited.  
- **Improvement**: Add stricter validation for user inputs to prevent invalid data entry.  

---
