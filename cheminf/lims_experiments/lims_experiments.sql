-- Create the database
CREATE DATABASE cheminf3_lims;
USE cheminf3_lims;

-- Create table for experiments
CREATE TABLE cheminf3_experiments (
    experiment_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_name VARCHAR(50) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE
);

-- Create table for samples
CREATE TABLE cheminf3_samples (
    sample_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_id INT,
    sample_code VARCHAR(20) UNIQUE NOT NULL,
    sample_type VARCHAR(50),
    collection_date DATE,
    FOREIGN KEY (experiment_id) REFERENCES cheminf3_experiments(experiment_id) ON DELETE CASCADE
);

-- Create table for measurements
CREATE TABLE cheminf3_measurements (
    measurement_id INT AUTO_INCREMENT PRIMARY KEY,
    sample_id INT,
    parameter VARCHAR(50) NOT NULL,
    value DECIMAL(10,3) NOT NULL,
    unit VARCHAR(10),
    measurement_date DATETIME,
    FOREIGN KEY (sample_id) REFERENCES cheminf3_samples(sample_id) ON DELETE CASCADE
);

-- Insert experiments
INSERT INTO cheminf3_experiments (experiment_name, description, start_date, end_date)
VALUES
    ('Exp-001', 'Water pH Analysis', '2025-03-01', '2025-03-05'),
    ('Exp-002', 'Metal Concentration', '2025-03-06', '2025-03-10'),
    ('Exp-003', 'Organic Compound Analysis', '2025-03-11', '2025-03-15'),
    ('Exp-004', 'Polymer Stability Study', '2025-03-16', '2025-03-20');

-- Insert samples
INSERT INTO cheminf3_samples (experiment_id, sample_code, sample_type, collection_date)
VALUES
    (1, 'S001', 'Water', '2025-03-02'),
    (1, 'S002', 'Water', '2025-03-02'),
    (1, 'S003', 'Water', '2025-03-03'),
    (1, 'S004', 'Water', '2025-03-04'),
    (1, 'S005', 'Water', '2025-03-05'),

    (2, 'S006', 'Metal Solution', '2025-03-06'),
    (2, 'S007', 'Metal Solution', '2025-03-07'),
    (2, 'S008', 'Metal Solution', '2025-03-08'),
    (2, 'S009', 'Metal Solution', '2025-03-09'),
    (2, 'S010', 'Metal Solution', '2025-03-10'),

    (3, 'S011', 'Organic Extract', '2025-03-11'),
    (3, 'S012', 'Organic Extract', '2025-03-12'),
    (3, 'S013', 'Organic Extract', '2025-03-13'),
    (3, 'S014', 'Organic Extract', '2025-03-14'),
    (3, 'S015', 'Organic Extract', '2025-03-15'),

    (4, 'S016', 'Polymer Solution', '2025-03-16'),
    (4, 'S017', 'Polymer Solution', '2025-03-17'),
    (4, 'S018', 'Polymer Solution', '2025-03-18'),
    (4, 'S019', 'Polymer Solution', '2025-03-19'),
    (4, 'S020', 'Polymer Solution', '2025-03-20');

-- Insert measurements
INSERT INTO cheminf3_measurements (sample_id, parameter, value, unit, measurement_date)
VALUES
    (1, 'pH', 7.2, '-', '2025-03-02 10:00:00'),
    (2, 'pH', 7.5, '-', '2025-03-02 11:00:00'),
    (3, 'pH', 7.1, '-', '2025-03-03 10:00:00'),
    (4, 'pH', 7.4, '-', '2025-03-04 12:00:00'),
    (5, 'pH', 7.3, '-', '2025-03-05 09:30:00'),

    (6, 'Fe Concentration', 0.45, 'mg/L', '2025-03-06 14:00:00'),
    (7, 'Fe Concentration', 0.48, 'mg/L', '2025-03-07 15:00:00'),
    (8, 'Fe Concentration', 0.43, 'mg/L', '2025-03-08 16:00:00'),
    (9, 'Fe Concentration', 0.50, 'mg/L', '2025-03-09 17:00:00'),
    (10, 'Fe Concentration', 0.46, 'mg/L', '2025-03-10 18:00:00'),

    (11, 'TOC', 12.5, 'mg/L', '2025-03-11 09:00:00'),
    (12, 'TOC', 13.0, 'mg/L', '2025-03-12 10:00:00'),
    (13, 'TOC', 11.8, 'mg/L', '2025-03-13 11:00:00'),
    (14, 'TOC', 12.2, 'mg/L', '2025-03-14 12:00:00'),
    (15, 'TOC', 12.7, 'mg/L', '2025-03-15 13:00:00'),

    (16, 'Viscosity', 3.5, 'cP', '2025-03-16 14:00:00'),
    (17, 'Viscosity', 3.7, 'cP', '2025-03-17 15:00:00'),
    (18, 'Viscosity', 3.6, 'cP', '2025-03-18 16:00:00'),
    (19, 'Viscosity', 3.4, 'cP', '2025-03-19 17:00:00'),
    (20, 'Viscosity', 3.8, 'cP', '2025-03-20 18:00:00');
