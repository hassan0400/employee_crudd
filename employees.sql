CREATE DATABASE IF NOT EXISTS employee_db;
USE employee_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255),
    city VARCHAR(100),
    photo VARCHAR(255)
);
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    date DATE NOT NULL,
    sign_in TIME,
    sign_out TIME,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
