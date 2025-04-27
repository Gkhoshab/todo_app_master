-- Populate users table with synthetic data (starting from ID 3)
INSERT INTO "user" (id, username, email, password_hash) VALUES
(3, 'alex_wilson', 'alex@example.com', 'pbkdf2:sha256:150000$JK4jnnX2$0b2cfa4e1ec1b3d419c847e0e574e6e5932a2581323b438c8ba8cf340e43d36d'),
(4, 'emily_chen', 'emily@example.com', 'pbkdf2:sha256:150000$TRG5tMwV$4c8b856ef92593183ef71f9320b7f1172658576e5fe3895493e7586c25cf9978'),
(5, 'sam_johnson', 'sam@example.com', 'pbkdf2:sha256:150000$Ht2ExR1s$b85b991dd28052037f535a7dc64b8c95a1e926829f4c5f3cc188c7eae9f9dcff');

-- Reset sequence to continue from the highest ID
SELECT setval(pg_get_serial_sequence('"user"', 'id'), 5);

-- Populate todos for alex_wilson
INSERT INTO todo (title, description, created_at, due_date, completed, priority, reminder_time, reminder_sent, user_id) VALUES
('Gym session', 'Leg day - squats, lunges, and deadlifts', '2024-03-12 07:30:00', '2024-03-13 18:00:00', TRUE, 1, NULL, FALSE, 3),
('Submit tax documents', 'Gather W-2s, receipts, and file taxes', '2024-02-15 11:20:00', '2024-04-15 23:59:59', FALSE, 3, '2024-04-10 09:00:00', FALSE, 3),
('Renew drivers license', 'Visit DMV with required documents', '2024-03-08 09:15:00', '2024-03-28 12:00:00', FALSE, 2, '2024-03-27 09:00:00', FALSE, 3),
('Fix kitchen sink', 'Replace leaky faucet', '2024-03-01 18:45:00', '2024-03-05 20:00:00', TRUE, 2, NULL, FALSE, 3),
('Weekly team meeting', 'Discuss project progress and challenges', '2024-03-15 09:00:00', '2024-03-15 10:30:00', FALSE, 2, '2024-03-15 09:15:00', FALSE, 3);

-- Populate todos for emily_chen
INSERT INTO todo (title, description, created_at, due_date, completed, priority, reminder_time, reminder_sent, user_id) VALUES
('Complete UX design mockups', 'Finalize homepage and product details page designs', '2024-03-01 10:30:00', '2024-03-10 17:00:00', TRUE, 3, NULL, FALSE, 4),
('Doctor appointment', 'Annual physical checkup with Dr. Johnson', '2024-03-08 15:00:00', '2024-04-05 14:30:00', FALSE, 2, '2024-04-04 14:30:00', FALSE, 4),
('Birthday gift for David', 'Find something related to photography or hiking', '2024-03-12 12:45:00', '2024-03-25 23:59:59', FALSE, 2, '2024-03-24 10:00:00', FALSE, 4),
('Research grad schools', 'Compare programs, requirements, and deadlines', '2024-02-20 19:20:00', '2024-04-30 23:59:59', FALSE, 1, NULL, FALSE, 4),
('Car maintenance', 'Oil change and tire rotation', '2024-03-05 08:30:00', '2024-03-15 18:00:00', TRUE, 2, '2024-03-14 10:00:00', TRUE, 4);

-- Populate todos for sam_johnson
INSERT INTO todo (title, description, created_at, due_date, completed, priority, reminder_time, reminder_sent, user_id) VALUES
('Client presentation', 'Prepare slides for quarterly review', '2024-03-01 13:15:00', '2024-03-15 15:00:00', FALSE, 3, '2024-03-14 15:00:00', FALSE, 5),
('Book club meeting', 'Finish reading "The Midnight Library" for discussion', '2024-03-05 21:00:00', '2024-03-20 19:00:00', FALSE, 1, '2024-03-19 18:00:00', FALSE, 5),
('Apartment hunting', 'Tour available units in downtown and riverside areas', '2024-03-10 10:00:00', '2024-04-30 23:59:59', FALSE, 2, NULL, FALSE, 5),
('Schedule pet vaccinations', 'Annual shots for Bella', '2024-03-07 16:30:00', '2024-03-31 18:00:00', FALSE, 2, '2024-03-29 09:00:00', FALSE, 5),
('Weekly grocery shopping', 'Check the refrigerator and make a list', '2024-03-14 08:00:00', '2024-03-16 12:00:00', TRUE, 1, NULL, FALSE, 5);

-- Reset sequence for todo table to continue after the inserted data
SELECT setval(pg_get_serial_sequence('todo', 'id'), (SELECT MAX(id) FROM todo)); 