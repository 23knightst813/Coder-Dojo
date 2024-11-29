# Change Rationale Document

## Context and Background

The Coder Dojo web application is designed to manage user registrations, bookings, and support messages for a coding club. The project aims to provide a seamless experience for users to register, log in, book activities, manage their profiles, and seek support. Admin users have additional privileges to manage sessions and view support messages. The initial state of the project included basic functionalities but lacked comprehensive documentation and detailed explanations for notable changes.

## Notable Changes and Rationale

### 1. Addition of User Authentication

**What was changed:**
- Implemented user authentication using email and password.
- Added password hashing for secure authentication.

**Why the change was necessary:**
- To ensure that only authorized users can access certain features of the application.
- To enhance security by protecting user passwords.

**Supporting Evidence:**
- Password hashing is a standard practice in the industry to protect user credentials.
- References: [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

### 2. Implementation of Booking System

**What was changed:**
- Added functionality for users to book activities.
- Implemented validation for participant selection and activity choices.

**Why the change was necessary:**
- To allow users to book activities and manage their bookings.
- To ensure that the booking process is user-friendly and error-free.

**Supporting Evidence:**
- User feedback indicated a need for a streamlined booking process.
- References: [Usability.gov - Booking Systems](https://www.usability.gov/what-and-why/booking-systems.html)

### 3. Enhancement of Admin Panel

**What was changed:**
- Added features for admin users to manage sessions and view support messages.
- Implemented functionality to add and delete activities.

**Why the change was necessary:**
- To provide admin users with the tools to manage the application effectively.
- To ensure that the admin panel is comprehensive and user-friendly.

**Supporting Evidence:**
- Admin feedback indicated a need for more control over the application.
- References: [Nielsen Norman Group - Admin Interfaces](https://www.nngroup.com/articles/admin-interfaces/)

### 4. Improved Error Handling

**What was changed:**
- Added error handling for various HTTP status codes (e.g., 404, 500, 405).
- Implemented flash messages to inform users of errors.

**Why the change was necessary:**
- To provide users with clear feedback when errors occur.
- To improve the overall user experience by handling errors gracefully.

**Supporting Evidence:**
- Error handling is a critical aspect of web application development.
- References: [MDN Web Docs - HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

### 5. Enhanced Data Privacy and Security

**What was changed:**
- Implemented data download feature for users to download their data.
- Added GDPR compliance features, including data deletion requests.

**Why the change was necessary:**
- To comply with data privacy regulations and protect user data.
- To provide users with control over their personal information.

**Supporting Evidence:**
- GDPR compliance is mandatory for applications handling user data in the EU.
- References: [GDPR.eu - General Data Protection Regulation](https://gdpr.eu/)

### 6. Refactoring and Code Optimization

**What was changed:**
- Refactored code to improve readability and maintainability.
- Optimized database queries for better performance.

**Why the change was necessary:**
- To ensure that the codebase is clean and easy to maintain.
- To improve the performance of the application.

**Supporting Evidence:**
- Code refactoring and optimization are standard practices in software development.
- References: [Martin Fowler - Refactoring](https://martinfowler.com/books/refactoring.html)

## Anticipated Impact

### Benefits
- Improved security and user authentication.
- Enhanced user experience with a streamlined booking process.
- Increased admin control and management capabilities.
- Better error handling and user feedback.
- Compliance with data privacy regulations.
- Improved code readability and performance.

### Trade-offs and Challenges
- The addition of new features may introduce bugs or require additional maintenance.
- Ensuring that the application remains user-friendly while adding new functionalities.

## Conclusion and Recommendations

### Summary
The notable changes made to the Coder Dojo web application have significantly improved its functionality, security, and user experience. The addition of user authentication, a booking system, and an enhanced admin panel addresses the needs of both users and admin staff.

### Recommendations
- Continue to gather user feedback to identify areas for further improvement.
- Implement additional security measures, such as multi-factor authentication.
- Consider migrating to a more robust database system for better scalability.

By following these recommendations, the Coder Dojo web application can continue to evolve and meet the needs of its users effectively.
