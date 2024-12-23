# Testing Log for Coder Dojo Web Application

## Test Case 1: User Registration
### Normal Data
- Input: 
  - Email: user@example.com
  - Password: SecurePass123
  - First Name: John
  - Last Name: Doe
- Expected Result: User registered successfully.
- Actual Result: User registered successfully.
- Status: Pass

### Erroneous Data
- Input: 
  - Email: user@example
  - Password: pass
  - First Name: 
  - Last Name: 
- Expected Result: Error messages for invalid email, weak password, and empty fields.
- Actual Result: Error messages displayed as expected.
- Status: Pass

### Extreme Data
- Input: 
  - Email: user@example.com
  - Password: A very long password with 1000 characters
  - First Name: John
  - Last Name: Doe
- Expected Result: User registered successfully or error message for password length.
- Actual Result: User registered successfully.
- Status: Pass

## Test Case 2: User Login
### Normal Data
- Input: 
  - Email: user@example.com
  - Password: SecurePass123
- Expected Result: User logged in successfully.
- Actual Result: User logged in successfully.
- Status: Pass

### Erroneous Data
- Input: 
  - Email: user@example.com
  - Password: WrongPass
- Expected Result: Error message for incorrect password.
- Actual Result: Error message displayed as expected.
- Status: Pass

### Extreme Data
- Input: 
  - Email: user@example.com
  - Password: A very long password with 1000 characters
- Expected Result: Error message for incorrect password.
- Actual Result: Error message displayed as expected.
- Status: Pass

## Test Case 3: Profile Editing
### Normal Data
- Input: 
  - First Name: Jane
  - Last Name: Smith
  - Password: NewSecurePass123
  - Participant Name: Participant1
  - Participant Age: 10
- Expected Result: Profile updated successfully.
- Actual Result: Profile updated successfully.
- Status: Pass

### Erroneous Data
- Input: 
  - First Name: 
  - Last Name: 
  - Password: 
  - Participant Name: 
  - Participant Age: 
- Expected Result: Error messages for empty fields.
- Actual Result: Error messages displayed as expected.
- Status: Pass

### Extreme Data
- Input: 
  - First Name: A very long name with 1000 characters
  - Last Name: A very long name with 1000 characters
  - Password: A very long password with 1000 characters
  - Participant Name: A very long name with 1000 characters
  - Participant Age: 1000
- Expected Result: Returns error since the age is too high.
- Actual Result: Returns error since the age is too high.
- Status: Pass

## Test Case 4: Support Request
### Normal Data
- Input: 
  - Subject: Need help
  - Message: I need help with my account.
- Expected Result: Support request submitted successfully.
- Actual Result: Support request submitted successfully.
- Status: Pass

### Erroneous Data
- Input: 
  - Subject: 
  - Message: 
- Expected Result: Error messages for empty fields.
- Actual Result: Error messages displayed as expected.
- Status: Pass

### Extreme Data
- Input: 
  - Subject: A very long subject with 1000 characters
  - Message: A very long message with 1000 characters
- Expected Result: Support request submitted successfully.
- Actual Result: Support request submitted successfully.
- Status: Pass

## Test Case 5: Booking Activities
### Normal Data
- Input: 
  - Participant: Participant1
  - Activity1: Coding Basics
  - Activity2: Advanced Python
  - Activity3: Robotics
- Expected Result: Booking created successfully.
- Actual Result: Booking created successfully.
- Status: Pass

### Erroneous Data
- Input: 
  - Participant: 
  - Activity1: 
  - Activity2: 
  - Activity3: 
- Expected Result: Error messages for empty fields.
- Actual Result: Error messages displayed as expected.
- Status: Pass

### Extreme Data
- Input: 
  - Participant: Participant1
  - Activity1: A very long activity name with 1000 characters
  - Activity2: A very long activity name with 1000 characters
  - Activity3: A very long activity name with 1000 characters
- Expected Result: Booking created successfully or error messages for field lengths.
- Actual Result: Booking created successfully.
- Status: Pass

## Test Case 6: Admin Panel Access
### Normal Data
- Input: 
  - Email: admin@codeclub.com
  - Password: adminpass
- Expected Result: Admin panel accessed successfully.
- Actual Result: Admin panel accessed successfully.
- Status: Pass

### Erroneous Data
- Input: 
  - Email: admin@codeclub.com
  - Password: wrongpass
- Expected Result: Error message for incorrect password.
- Actual Result: Error message displayed as expected.
- Status: Pass

### Extreme Data
- Input: 
  - Email: admin@codeclub.com
  - Password: A very long password with 1000 characters
- Expected Result: Error message for incorrect password.
- Actual Result: Error message displayed as expected.
- Status: Pass

## Test Case 7: Database and Backend Setup
### Unit Testing, White Box Testing
- Ensure database tables for events, bookings, users, and activities are created.
- Perform unit tests on core backend functions to confirm data storage and retrieval operations work correctly.
- Status: Pass

## Test Case 8: User Registration Page
### Black Box, Functional Test, Usability Test
- Frontend registration form, backend user creation functions.
- Verify that new users can create accounts with proper data validation and security measures.
- Status: Pass

## Test Case 9: Account Creation Confirmation
### Black Box, Functional Test, Usability Test
- Successful user registration process.
- Ensure users receive confirmation upon account creation and the process is user-friendly.
- Status: Pass

## Test Case 10: User Login and Account Management
### White Box, Functional Test, Security Test
- User accounts exist in the database.
- Test login functionality, profile editing, and password reset features for correctness and security.
- Status: Pass

## Test Case 11: Event Listing
### Black Box, Functional Test, Usability Test
- Events are created and stored in the database.
- Verify that events are listed correctly and the interface is user-friendly.
- Status: Pass

## Test Case 12: Event Information Display on Event Details Page
### Black Box, Functional Test, Usability Test
- Individual event data available.
- Ensure event details are displayed accurately and comprehensively on the event details page.
- Status: Pass

## Test Case 13: Booking Button
### Black Box, Functional Test, Integration Test
- Booking system integrated with events and users.
- Verify that the booking button functions correctly and integrates with the backend booking system.
- Status: Pass

## Test Case 14: Activity List
### Usability Test, Performance Test
- Activities are loaded from the database.
- Ensure the activity list is easy to use and loads efficiently.
- Status: Pass

## Test Case 15: Booking Confirmation
### Black Box, Functional Test, Integration Test
- Successful booking process.
- Confirm that users receive booking confirmations and that bookings are correctly recorded in the system.
- Status: Pass

## Test Case 16: Booking Management Page
### Black Box, Functional Test, Usability Test
- User is logged in and has existing bookings.
- Ensure users can view, manage, and cancel their bookings effectively.
- Status: Pass

## Test Case 17: Cancel Booking
### Black Box, Functional Test, Integration Test
- Existing bookings to cancel.
- Verify that bookings can be canceled and that the system updates accordingly.
- Status: Pass

## Test Case 18: Waitlist Management
### Black Box, Functional Test, Performance Test
- Event is fully booked and waitlist functionality is enabled.
- Ensure users can join the waitlist and that the system handles waitlist operations efficiently.
- Status: Pass


## Test Case 19: Data Privacy and Deletion (GDPR Compliance)
### Black Box, Functional Test, Integration Test
- User data exists in the system.
- Verify that users can manage their data privacy settings and request data deletion in compliance with GDPR.
- Status: Pass

