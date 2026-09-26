CREATE DATABASE IF NOT EXISTS staffsync;
USE staffsync;

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INT,
    hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);


INSERT INTO departments (name) VALUES ('Engineering'), ('Human Resources'), ('Sales');
INSERT INTO employees (name, email, department_id) VALUES
('Ana Garcia', 'ana@staffsync.com', 1),
('Carlos Lopez', 'carlos@staffsync.com', 2);
