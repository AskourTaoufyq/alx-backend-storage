-- create a table users with attributes id, email, name and country. 
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email CHAR(255) NOT NULL UNIQUE,
    name CHAR(255),
    country ENUM('US', 'CO', 'TN') DEFAULT 'US'
);
