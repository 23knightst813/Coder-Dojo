-- Insert test data into the users table
INSERT INTO users (email, password, first_name, last_name, is_admin) VALUES
('admin@codeclub.com', 'adminpass', 'Admin', 'User', TRUE),
('a@a.co.fortei', 'fortnite', 'John', 'Doe', TRUE),
('jane.smith@example.com', 'securepass', 'Jane', 'Smith', FALSE);

-- Insert test data into the participants table
INSERT INTO participants (user_id, name, age) VALUES
(2, 'John Doe', 14),
(3, 'Jane Smith', 12);

-- Insert test data into the activities table
INSERT INTO activities (activity_name) VALUES
('Coding Basics'),
('Advanced Python'),
('Robotics');

-- Insert test data into the bookings table
INSERT INTO bookings (participant_id, user_id, activity1_id, activity2_id, activity3_id,overflow_count) VALUES
(1 , 2, 1, 2, 3,1),
(1 , 2, 1, 2, 3,2),
(2, 2, NULL, NULL);



-- Insert test user if not exists
INSERT OR IGNORE INTO users (user_id, email, password, first_name, last_name, is_admin) 
VALUES (3, 'test@example.com', 'hashed_password', 'Test', 'User', 1);

-- Insert sample support tickets
INSERT INTO support (user_id, support) VALUES 
(1, 'Need help with activity booking system'),
(1, 'How do I update my participant information?'),
(1, 'Cannot access my account settings'),
(1, 'Request for activity schedule change'),
(1, 'Technical issue with registration form');

-- Insert with specific timestamps for testing
INSERT INTO support (user_id, support, created_at) VALUES 
(1, 'Urgent support needed', datetime('now', '-2 days')),
(1, 'Follow-up question', datetime('now', '-1 day')),
(1, 'Issue resolved', datetime('now'));