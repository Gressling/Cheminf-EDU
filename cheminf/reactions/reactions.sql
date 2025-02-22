-- 2. Create reactions table
CREATE TABLE cheminf3_reactions (
    ReactionID INT AUTO_INCREMENT PRIMARY KEY,
    ReactionName VARCHAR(255),
    ReactionDescription TEXT  -- Optional descriptive details about the reaction
);

-- 3. Create reaction participants table (junction between reactions and molecules)
CREATE TABLE cheminf3_reactionparticipants (
    ReactionID INT,
    MoleculeID INT,
    Role VARCHAR(50),  -- e.g., 'reactant', 'product', 'catalyst', etc.
    StoichiometricCoefficient DECIMAL(10,3),  -- Supports non-integer values if needed
    PRIMARY KEY (ReactionID, MoleculeID, Role),
    FOREIGN KEY (ReactionID) REFERENCES cheminf3_reactions(ReactionID),
    FOREIGN KEY (MoleculeID) REFERENCES cheminf3_molecules(id)
);

INSERT INTO cheminf3_reactions (ReactionName, ReactionDescription)
VALUES ('Aspirin Synthesis', 'Synthesis of acetylsalicylic acid (aspirin) from salicylic acid and acetic anhydride with an acid catalyst.');

-- Salicylic Acid as reactant
INSERT INTO cheminf3_reactionparticipants (ReactionID, MoleculeID, Role, StoichiometricCoefficient)
VALUES (1, 1, 'reactant', 1.0);

-- Acetic Anhydride as reactant
INSERT INTO cheminf3_reactionparticipants (ReactionID, MoleculeID, Role, StoichiometricCoefficient)
VALUES (1, 2, 'reactant', 1.0);

-- Sulfuric Acid as catalyst (coefficient is illustrative)
INSERT INTO cheminf3_reactionparticipants (ReactionID, MoleculeID, Role, StoichiometricCoefficient)
VALUES (1, 5, 'catalyst', 0.1);

-- Acetylsalicylic Acid (Aspirin) as product
INSERT INTO cheminf3_reactionparticipants (ReactionID, MoleculeID, Role, StoichiometricCoefficient)
VALUES (1, 3, 'product', 1.0);

-- Acetic Acid as product
INSERT INTO cheminf3_reactionparticipants (ReactionID, MoleculeID, Role, StoichiometricCoefficient)
VALUES (1, 4, 'product', 1.0);


SELECT 
  CONCAT(
    (SELECT GROUP_CONCAT(
              CASE 
                WHEN StoichiometricCoefficient <> 1 
                THEN CONCAT(StoichiometricCoefficient, ' ', MoleculeUpacName) 
                ELSE MoleculeUpacName 
              END
              SEPARATOR ' + ')
     FROM cheminf3_reactionparticipants rp 
     JOIN cheminf3_molecules m ON rp.MoleculeID = m.id
     WHERE rp.ReactionID = 1 AND rp.Role = 'reactant'),
    ' -> ',
    (SELECT GROUP_CONCAT(
              CASE 
                WHEN StoichiometricCoefficient <> 1 
                THEN CONCAT(StoichiometricCoefficient, ' ', MoleculeUpacName) 
                ELSE MoleculeUpacName 
              END
              SEPARATOR ' + ')
     FROM cheminf3_reactionparticipants rp 
     JOIN cheminf3_molecules m ON rp.MoleculeID = m.id
     WHERE rp.ReactionID = 1 AND rp.Role = 'product')
  ) AS ChemicalEquation;

---> Salicylic Acid + Acetic Anhydride -> Acetylsalicylic Acid (Aspirin) + Acetic Acid

SELECT 
  r.ReactionName,
  r.ReactionDescription,
  CONCAT(
    'Reactants: ', GROUP_CONCAT(CASE WHEN rp.Role = 'reactant' 
                                      THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                      END SEPARATOR ' + '),
    ' | Products: ', GROUP_CONCAT(CASE WHEN rp.Role = 'product' 
                                      THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                      END SEPARATOR ' + '),
    ' | Catalysts: ', GROUP_CONCAT(CASE WHEN rp.Role = 'catalyst' 
                                      THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                      END SEPARATOR ', ')
  ) AS ReactionEquation
FROM cheminf3_reactions r
JOIN cheminf3_reactionparticipants rp ON r.ReactionID = rp.ReactionID
JOIN cheminf3_molecules m ON rp.MoleculeID = m.id
WHERE r.ReactionID = 1
GROUP BY r.ReactionID, r.ReactionName, r.ReactionDescription;

--->	ReactionName	    ReactionDescription	                                                                                              ReactionEquation
--->	Aspirin Synthesis	Synthesis of acetylsalicylic acid (aspirin) from salicylic acid and acetic anhydride with an acid catalyst.	Reactants: 1.000 Salicylic Acid (Oc1ccccc1C(=O)O) + 1.000 Acetic Anhydride (CC(=O)OC(=O)C) | Products: 1.000 Acetylsalicylic Acid (Aspirin) (CC(=O)Oc1ccccc1C(=O)O) + 1.000 Acetic Acid (CC(=O)O) | Catalysts: 0.100 Sulfuric Acid (OS(=O)(=O)O)