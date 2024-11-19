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
INSERT INTO bookings (participant_id, activity1_id, activity2_id, activity3_id) VALUES
(1, 1, 2, 3),
(2, 2, NULL, NULL);
