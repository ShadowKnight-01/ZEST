-- Disable triggers/constraints temporarily to drop tables cleanly
SET session_replication_role = 'replica';
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;
SET session_replication_role = 'origin';

-- Create USERS table
CREATE TABLE users (
    id SERIAL,                              -- just a num first person id is 1 and he tenth is 10
    user_id VARCHAR(20) NOT NULL,           -- user id get generated auto maticly with str(uuid.uuid4())
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(20),
    age INT,
    course VARCHAR(100),
    education VARCHAR(100),
    place VARCHAR(100),
    state VARCHAR(50),
    city VARCHAR(50),
    profile_pic VARCHAR(255),
    user_or_admin VARCHAR(20) DEFAULT 'users' CHECK (user_or_admin IN ('users', 'admin')), 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id),                  -- Make user_id as primary key
    CONSTRAINT uk_username UNIQUE (username),
    CONSTRAINT uk_email UNIQUE (email)
);

-- Create POSTS table
CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL, -- Changed to VARCHAR(20) to match parent table's PK type
    content TEXT NOT NULL,
    image VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

-- Create MESSAGES table
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY, -- Creates a unique, auto-incrementing ID for every new message
    sender_id VARCHAR(20) NOT NULL,   -- Changed to VARCHAR(20) to match parent table's PK type
    receiver_id VARCHAR(20) NOT NULL, -- Changed to VARCHAR(20) to match parent table's PK type
    message TEXT NOT NULL, -- Stores the actual text content of the message. Cannot be empty.
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Automatically logs the exact date, time, and timezone when the row is created

    FOREIGN KEY (sender_id) -- Defines the relationship for the sender
    REFERENCES users(user_id) -- Links the sender_id back to a valid user_id in the 'users' table
    ON DELETE CASCADE, -- If the sender is deleted from the users table, automatically delete their messages here

    FOREIGN KEY (receiver_id) -- Defines the relationship for the receiver
    REFERENCES users(user_id) -- Links the receiver_id back to a valid user_id in the 'users' table
    ON DELETE CASCADE -- If the receiver is deleted from the users table, automatically delete the messages sent to them
);