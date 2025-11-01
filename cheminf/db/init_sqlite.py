"""
SQLite Database Initialization Script
This script creates and initializes the SQLite database with all required tables and sample data.
"""

import sqlite3
import os
from pathlib import Path

# Define database path
DB_PATH = Path(__file__).parent.parent.parent / "cheminf_edu.db"

def create_database():
    """Create SQLite database and all required tables with sample data."""
    
    # Remove existing database if it exists
    if DB_PATH.exists():
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Create molecules table
        cursor.execute("""
            CREATE TABLE cheminf3_molecules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                MoleculeUpacName CHAR(200) NOT NULL,
                SMILES VARCHAR(255)
            )
        """)
        
        # Create reactions table
        cursor.execute("""
            CREATE TABLE cheminf3_reactions (
                ReactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                ReactionName VARCHAR(255),
                ReactionDescription TEXT
            )
        """)
        
        # Create reaction participants table
        cursor.execute("""
            CREATE TABLE cheminf3_reactionparticipants (
                ReactionID INTEGER,
                MoleculeID INTEGER,
                Role VARCHAR(50),
                StoichiometricCoefficient DECIMAL(10,3),
                PRIMARY KEY (ReactionID, MoleculeID, Role),
                FOREIGN KEY (ReactionID) REFERENCES cheminf3_reactions(ReactionID),
                FOREIGN KEY (MoleculeID) REFERENCES cheminf3_molecules(id)
            )
        """)
        
        # Create inventory table
        cursor.execute("""
            CREATE TABLE cheminf3_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                MoleculeUpacName VARCHAR(255) NOT NULL UNIQUE,
                amount INTEGER NOT NULL CHECK (amount >= 0),
                unit VARCHAR(20)
            )
        """)
        
        # Create project table
        cursor.execute("""
            CREATE TABLE cheminf3_project (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL
            )
        """)
        
        # Create task table
        cursor.execute("""
            CREATE TABLE cheminf3_task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                description VARCHAR(255) NOT NULL,
                content TEXT,
                FOREIGN KEY (project_id) REFERENCES cheminf3_project(id) ON DELETE CASCADE
            )
        """)
        
        # Create experiments table
        cursor.execute("""
            CREATE TABLE cheminf3_experiments (
                experiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name VARCHAR(50) NOT NULL,
                description TEXT,
                start_date DATE,
                end_date DATE
            )
        """)
        
        # Create samples table
        cursor.execute("""
            CREATE TABLE cheminf3_samples (
                sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id INTEGER,
                sample_code VARCHAR(20) UNIQUE NOT NULL,
                sample_type VARCHAR(50),
                collection_date DATE,
                FOREIGN KEY (experiment_id) REFERENCES cheminf3_experiments(experiment_id) ON DELETE CASCADE
            )
        """)
        
        # Create measurements table
        cursor.execute("""
            CREATE TABLE cheminf3_measurements (
                measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id INTEGER,
                parameter VARCHAR(50) NOT NULL,
                value DECIMAL(10,3) NOT NULL,
                unit VARCHAR(10),
                measurement_date DATETIME,
                FOREIGN KEY (sample_id) REFERENCES cheminf3_samples(sample_id) ON DELETE CASCADE
            )
        """)
        
        # Insert molecules data
        molecules_data = [
            ('Salicylic Acid', 'Oc1ccccc1C(=O)O'),
            ('Acetic Anhydride', 'CC(=O)OC(=O)C'),
            ('Acetylsalicylic Acid (Aspirin)', 'CC(=O)Oc1ccccc1C(=O)O'),
            ('Acetic Acid', 'CC(=O)O'),
            ('Sulfuric Acid', 'OS(=O)(=O)O'),
            ('Glacial Acetic Acid', 'CC(=O)O'),
            ('Ethanol', 'CCO'),
            ('Methanol', 'CO'),
            ('Water', 'O'),
            ('Sodium Bicarbonate', 'O=C(O)[O-].[Na+]'),
            ('Sodium Acetate', 'CC(=O)[O-].[Na+]'),
            ('Dichloromethane', 'ClCCl'),
            ('Ethyl Acetate', 'CCOC(=O)C'),
            ('Diethyl Ether', 'CCOCC'),
            ('Hexane', 'CCCCCC'),
            ('Toluene', 'Cc1ccccc1'),
            ('Acetone', 'CC(=O)C'),
            ('Isopropanol', 'CC(O)C'),
            ('Acetonitrile', 'CC#N'),
            ('Dimethyl Sulfoxide (DMSO)', 'CS(=O)C'),
            ('Propionic Acid', 'CCC(=O)O'),
            ('Butyric Acid', 'CCCC(=O)O'),
            ('Potassium Carbonate', '[K+].[K+].C(=O)([O-])[O-]'),
            ('Magnesium Sulfate', '[Mg+2].[O-]S(=O)(=O)[O-]'),
            ('Calcium Carbonate', '[Ca+2].C(=O)([O-])[O-]'),
            ('Sodium Hydroxide', '[Na+].[OH-]'),
            ('Potassium Hydroxide', '[K+].[OH-]'),
            ('Pyridine', 'c1ccncc1'),
            ('p-Toluenesulfonic Acid', 'Cc1ccc(cc1)S(=O)(=O)O'),
            ('Hydrochloric Acid', '[H]Cl'),
            ('Acetyl Chloride', 'CC(=O)Cl'),
            ('Benzoic Acid', 'c1ccc(cc1)C(=O)O'),
            ('Benzaldehyde', 'c1ccccc1C=O'),
            ('Salicylaldehyde', 'O=Cc1ccccc1O'),
            ('Methyl Salicylate', 'COC(=O)c1ccccc1O'),
            ('4-Aminobenzoic Acid', 'Nc1ccc(cc1)C(=O)O'),
            ('2,4-Dihydroxybenzoic Acid', 'O=C(O)c1c(O)ccc(O)c1'),
            ('3-Acetylsalicylic Acid', 'O=C(O)c1c(O)c(C(=O)C)cccc1'),
            ('Phenol', 'Oc1ccccc1'),
            ('Aniline', 'Nc1ccccc1')
        ]
        
        cursor.executemany("INSERT INTO cheminf3_molecules (MoleculeUpacName, SMILES) VALUES (?, ?)", molecules_data)
        
        # Insert reaction data
        cursor.execute("""
            INSERT INTO cheminf3_reactions (ReactionName, ReactionDescription)
            VALUES ('Aspirin Synthesis', 'Synthesis of acetylsalicylic acid (aspirin) from salicylic acid and acetic anhydride with an acid catalyst.')
        """)
        
        # Insert reaction participants
        reaction_participants = [
            (1, 1, 'reactant', 1.0),  # Salicylic Acid
            (1, 2, 'reactant', 1.0),  # Acetic Anhydride
            (1, 5, 'catalyst', 0.1),  # Sulfuric Acid
            (1, 3, 'product', 1.0),   # Aspirin
            (1, 4, 'product', 1.0)    # Acetic Acid
        ]
        
        cursor.executemany("""
            INSERT INTO cheminf3_reactionparticipants (ReactionID, MoleculeID, Role, StoichiometricCoefficient)
            VALUES (?, ?, ?, ?)
        """, reaction_participants)
        
        # Insert inventory data
        inventory_data = [
            ('Methanol', 500, 'ml'),
            ('Ethanol', 300, 'ml'),
            ('Acetone', 200, 'ml'),
            ('Toluene', 150, 'ml'),
            ('Chloroform', 100, 'ml')
        ]
        
        cursor.executemany("INSERT INTO cheminf3_inventory (MoleculeUpacName, amount, unit) VALUES (?, ?, ?)", inventory_data)
        
        # Insert project data
        cursor.execute("INSERT INTO cheminf3_project (name) VALUES ('Aspirin synthesis optimization')")
        
        # Insert task data
        tasks_data = [
            (1, 'Optimize step 1', '{"type": "optimization", "step": 1, "parameters": {"temperature": 100, "time": 10}}'),
            (1, 'Optimize step 2', '{"type": "optimization", "step": 2, "parameters": {"temperature": 120, "time": 20}}'),
            (1, 'Optimize step 3', '{"type": "optimization", "step": 3, "parameters": {"temperature": 140, "time": 30}}')
        ]
        
        cursor.executemany("INSERT INTO cheminf3_task (project_id, description, content) VALUES (?, ?, ?)", tasks_data)
        
        # Insert experiments data
        experiments_data = [
            ('Exp-001', 'Water pH Analysis', '2025-03-01', '2025-03-05'),
            ('Exp-002', 'Metal Concentration', '2025-03-06', '2025-03-10'),
            ('Exp-003', 'Organic Compound Analysis', '2025-03-11', '2025-03-15'),
            ('Exp-004', 'Polymer Stability Study', '2025-03-16', '2025-03-20')
        ]
        
        cursor.executemany("""
            INSERT INTO cheminf3_experiments (experiment_name, description, start_date, end_date)
            VALUES (?, ?, ?, ?)
        """, experiments_data)
        
        # Insert samples data
        samples_data = [
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
            (4, 'S020', 'Polymer Solution', '2025-03-20')
        ]
        
        cursor.executemany("""
            INSERT INTO cheminf3_samples (experiment_id, sample_code, sample_type, collection_date)
            VALUES (?, ?, ?, ?)
        """, samples_data)
        
        # Insert measurements data
        measurements_data = [
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
            (20, 'Viscosity', 3.8, 'cP', '2025-03-20 18:00:00')
        ]
        
        cursor.executemany("""
            INSERT INTO cheminf3_measurements (sample_id, parameter, value, unit, measurement_date)
            VALUES (?, ?, ?, ?, ?)
        """, measurements_data)
        
        conn.commit()
        print(f"[SUCCESS] SQLite database created successfully at: {DB_PATH}")
        print(f"[INFO] Created {len(molecules_data)} molecules")
        print(f"[INFO] Created 1 reaction with 5 participants")
        print(f"[INFO] Created {len(inventory_data)} inventory items")
        print(f"[INFO] Created 1 project with 3 tasks")
        print(f"[INFO] Created {len(experiments_data)} experiments")
        print(f"[INFO] Created {len(samples_data)} samples")
        print(f"[INFO] Created {len(measurements_data)} measurements")
        
    except Exception as e:
        print(f"[ERROR] Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()