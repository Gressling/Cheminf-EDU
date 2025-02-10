CREATE TABLE cheminf3_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    MoleculeUpacName VARCHAR(255) NOT NULL UNIQUE,
    amount INT NOT NULL CHECK (amount >= 0)
);

-- Example data for solvents
INSERT INTO cheminf3_inventory (MoleculeUpacName, amount) VALUES
    ('Methanol', 500),
    ('Ethanol', 300),
    ('Acetone', 200),
    ('Toluene', 150),
    ('Chloroform', 100);

ALTER TABLE cheminf3_inventory 
ADD COLUMN unit VARCHAR(20);

UPDATE cheminf3_inventory 
SET unit = 'ml';

