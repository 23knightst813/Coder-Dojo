## Change Rational

### 1 Booking system

**What Changed**
- Added functionality for users to book activities and cancel bookings, and automatically join a waiting list when needed.  
- Provided input validation
- Added activity preferences for the user to select when booking

**Why**
- The brief states that there's a need for a system to manage bookings since there has been a recent influx in booking
- Activity preferences help organisers prepare resources effectively

---

## 2 User Authentication

**What Changed**
    - User authentication using email and password.  
    - Allows users to log in and save their details
    - Added password hashing for secure storage of credentials.

**Why**

    - The brief states *Create user accounts to speed up the booking process*

---

## 3 Admin Panel

**What Changed**

- Enabled admin users to manage events, monitor bookings, and view user activity preferences.  
- Added options for creating and deleting events.  

**Why**  

- The brief outlines the organiser’s need to publish event details and manage resource planning. The admin panel empowers organisers to perform these tasks effectively.

---

## 4 Improved Error Handling and Input Validation

**What Changed**

- Added error handling for 500 and 405 status codes.
- Enhanced input validation for various forms, including age validation for participants.
- Updated error messages for better clarity.
- Implemented improved validation and flash messages for booking functionality.


**Why**

- To make the codebase easier to understand and maintain for current and future developers.
- To enhance the user interface for a more consistent and visually appealing experience.

---

## 5 Meeting GDPR

**What Chaned**

- Implemented a feature allowing users to download their data.  
- Implemented a feature allowing users to delete their data.

**Why**

- To meet professional guidelines and legislation