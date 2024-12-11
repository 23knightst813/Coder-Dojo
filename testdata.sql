
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


-- Insert with specific timestamps for testing
INSERT INTO support (user_id, support, created_at) VALUES 
(1, 'Urgent support needed', datetime('now', '-2 days')),
(1, 'Follow-up question', datetime('now', '-1 day')),
(1, 'Issue resolved', datetime('now'));