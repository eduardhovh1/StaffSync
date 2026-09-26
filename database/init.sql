CREATE DATABASE IF NOT EXISTS staffsync;
USE staffsync;

CREATE TABLE departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE trabajadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    departamento_id INT,
    fecha_contratacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE SET NULL
);


INSERT INTO departamentos (nombre) VALUES ('Ingeniería'), ('Recursos Humanos'), ('Ventas');
INSERT INTO trabajadores (nombre, email, departamento_id) VALUES 
('Ana García', 'ana@staffsync.com', 1),
('Carlos López', 'carlos@staffsync.com', 2);