
CREATE DATABASE library_db;
USE library_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(10)
);

INSERT INTO users VALUES
(1,'adm','adm','admin'),
(2,'user','user','user');

CREATE TABLE books (
    serial_no INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    author VARCHAR(100),
    category VARCHAR(50),
    status VARCHAR(20),
    procurement_date DATE
);

CREATE TABLE memberships (
    membership_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20),
    aadhar VARCHAR(20),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    pending_fine INT DEFAULT 0
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    serial_no INT,
    membership_id INT,
    issue_date DATE,
    return_date DATE,
    actual_return_date DATE,
    fine INT,
    status VARCHAR(20)
);
