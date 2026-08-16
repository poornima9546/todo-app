-- Create the Todo database
CREATE DATABASE IF NOT EXISTS todo_db;

-- Select the Todo database
USE todo_db;

-- Create the todos table
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
