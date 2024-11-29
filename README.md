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

