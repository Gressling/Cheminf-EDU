CREATE TABLE cheminf3_molecules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    MoleculeUpacName CHAR(200) NOT NULL
);

-- Insert molecules related to aspirin synthesis and common laboratory reagents/solvents

INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Salicylic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Acetic Anhydride');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Acetylsalicylic Acid (Aspirin)');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Acetic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Sulfuric Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Glacial Acetic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Ethanol');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Methanol');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Water');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Sodium Bicarbonate');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Sodium Acetate');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Dichloromethane');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Ethyl Acetate');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Diethyl Ether');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Hexane');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Toluene');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Acetone');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Isopropanol');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Acetonitrile');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Dimethyl Sulfoxide (DMSO)');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Propionic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Butyric Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Potassium Carbonate');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Magnesium Sulfate');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Calcium Carbonate');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Sodium Hydroxide');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Potassium Hydroxide');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Pyridine');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('p-Toluenesulfonic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Hydrochloric Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Acetyl Chloride');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Benzoic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Benzaldehyde');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Salicylaldehyde');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Methyl Salicylate');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('4-Aminobenzoic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('2,4-Dihydroxybenzoic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('3-Acetylsalicylic Acid');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Phenol');
INSERT INTO cheminf3_molecules (MoleculeUpacName) VALUES ('Aniline');

-- For the molecules table:
ALTER TABLE cheminf3_molecules
ADD COLUMN SMILES VARCHAR(255) AFTER MoleculeUpacName;

-- 1. Salicylic Acid (2‐hydroxybenzoic acid)
UPDATE cheminf3_molecules
  SET SMILES = 'Oc1ccccc1C(=O)O'
WHERE MoleculeUpacName = 'Salicylic Acid';

-- 2. Acetic Anhydride
UPDATE cheminf3_molecules
  SET SMILES = 'CC(=O)OC(=O)C'
WHERE MoleculeUpacName = 'Acetic Anhydride';

-- 3. Acetylsalicylic Acid (Aspirin)
UPDATE cheminf3_molecules
  SET SMILES = 'CC(=O)Oc1ccccc1C(=O)O'
WHERE MoleculeUpacName = 'Acetylsalicylic Acid (Aspirin)';

-- 4. Acetic Acid
UPDATE cheminf3_molecules
  SET SMILES = 'CC(=O)O'
WHERE MoleculeUpacName = 'Acetic Acid';

-- 5. Sulfuric Acid
UPDATE cheminf3_molecules
  SET SMILES = 'OS(=O)(=O)O'
WHERE MoleculeUpacName = 'Sulfuric Acid';

-- 6. Glacial Acetic Acid 
-- (glacial acetic acid is essentially pure acetic acid)
UPDATE cheminf3_molecules
  SET SMILES = 'CC(=O)O'
WHERE MoleculeUpacName = 'Glacial Acetic Acid';

-- 7. Ethanol
UPDATE cheminf3_molecules
  SET SMILES = 'CCO'
WHERE MoleculeUpacName = 'Ethanol';

-- 8. Methanol
UPDATE cheminf3_molecules
  SET SMILES = 'CO'
WHERE MoleculeUpacName = 'Methanol';

-- 9. Water
UPDATE cheminf3_molecules
  SET SMILES = 'O'
WHERE MoleculeUpacName = 'Water';

-- 10. Sodium Bicarbonate 
-- (represented as the ionic pair of bicarbonate and sodium)
UPDATE cheminf3_molecules
  SET SMILES = 'O=C(O)[O-].[Na+]'
WHERE MoleculeUpacName = 'Sodium Bicarbonate';

-- 11. Sodium Acetate
UPDATE cheminf3_molecules
  SET SMILES = 'CC(=O)[O-].[Na+]'
WHERE MoleculeUpacName = 'Sodium Acetate';

-- 12. Dichloromethane
UPDATE cheminf3_molecules
  SET SMILES = 'ClCCl'
WHERE MoleculeUpacName = 'Dichloromethane';

-- 13. Ethyl Acetate
UPDATE cheminf3_molecules
  SET SMILES = 'CCOC(=O)C'
WHERE MoleculeUpacName = 'Ethyl Acetate';

-- 14. Diethyl Ether
UPDATE cheminf3_molecules
  SET SMILES = 'CCOCC'
WHERE MoleculeUpacName = 'Diethyl Ether';

-- 15. Hexane
UPDATE cheminf3_molecules
  SET SMILES = 'CCCCCC'
WHERE MoleculeUpacName = 'Hexane';

-- 16. Toluene
UPDATE cheminf3_molecules
  SET SMILES = 'Cc1ccccc1'
WHERE MoleculeUpacName = 'Toluene';

-- 17. Acetone
UPDATE cheminf3_molecules
  SET SMILES = 'CC(=O)C'
WHERE MoleculeUpacName = 'Acetone';

-- 18. Isopropanol
UPDATE cheminf3_molecules
  SET SMILES = 'CC(O)C'
WHERE MoleculeUpacName = 'Isopropanol';

-- 19. Acetonitrile
UPDATE cheminf3_molecules
  SET SMILES = 'CC#N'
WHERE MoleculeUpacName = 'Acetonitrile';

-- 20. Dimethyl Sulfoxide (DMSO)
UPDATE cheminf3_molecules
  SET SMILES = 'CS(=O)C'
WHERE MoleculeUpacName = 'Dimethyl Sulfoxide (DMSO)';

-- 21. Propionic Acid
UPDATE cheminf3_molecules
  SET SMILES = 'CCC(=O)O'
WHERE MoleculeUpacName = 'Propionic Acid';

-- 22. Butyric Acid
UPDATE cheminf3_molecules
  SET SMILES = 'CCCC(=O)O'
WHERE MoleculeUpacName = 'Butyric Acid';

-- 23. Potassium Carbonate 
-- (carbonate ion is represented as C(=O)([O-])[O-] with two K+ counterions)
UPDATE cheminf3_molecules
  SET SMILES = '[K+].[K+].C(=O)([O-])[O-]'
WHERE MoleculeUpacName = 'Potassium Carbonate';

-- 24. Magnesium Sulfate 
-- (sulfate as [O-]S(=O)(=O)[O-] paired with Mg2+)
UPDATE cheminf3_molecules
  SET SMILES = '[Mg+2].[O-]S(=O)(=O)[O-]'
WHERE MoleculeUpacName = 'Magnesium Sulfate';

-- 25. Calcium Carbonate
UPDATE cheminf3_molecules
  SET SMILES = '[Ca+2].C(=O)([O-])[O-]'
WHERE MoleculeUpacName = 'Calcium Carbonate';

-- 26. Sodium Hydroxide
UPDATE cheminf3_molecules
  SET SMILES = '[Na+].[OH-]'
WHERE MoleculeUpacName = 'Sodium Hydroxide';

-- 27. Potassium Hydroxide
UPDATE cheminf3_molecules
  SET SMILES = '[K+].[OH-]'
WHERE MoleculeUpacName = 'Potassium Hydroxide';

-- 28. Pyridine
UPDATE cheminf3_molecules
  SET SMILES = 'c1ccncc1'
WHERE MoleculeUpacName = 'Pyridine';

-- 29. p-Toluenesulfonic Acid
UPDATE cheminf3_molecules
  SET SMILES = 'Cc1ccc(cc1)S(=O)(=O)O'
WHERE MoleculeUpacName = 'p-Toluenesulfonic Acid';

-- 30. Hydrochloric Acid
UPDATE cheminf3_molecules
  SET SMILES = '[H]Cl'
WHERE MoleculeUpacName = 'Hydrochloric Acid';

-- 31. Acetyl Chloride
UPDATE cheminf3_molecules
  SET SMILES = 'CC(=O)Cl'
WHERE MoleculeUpacName = 'Acetyl Chloride';

-- 32. Benzoic Acid
UPDATE cheminf3_molecules
  SET SMILES = 'c1ccc(cc1)C(=O)O'
WHERE MoleculeUpacName = 'Benzoic Acid';

-- 33. Benzaldehyde
UPDATE cheminf3_molecules
  SET SMILES = 'c1ccccc1C=O'
WHERE MoleculeUpacName = 'Benzaldehyde';

-- 34. Salicylaldehyde
UPDATE cheminf3_molecules
  SET SMILES = 'O=Cc1ccccc1O'
WHERE MoleculeUpacName = 'Salicylaldehyde';

-- 35. Methyl Salicylate
UPDATE cheminf3_molecules
  SET SMILES = 'COC(=O)c1ccccc1O'
WHERE MoleculeUpacName = 'Methyl Salicylate';

-- 36. 4-Aminobenzoic Acid
UPDATE cheminf3_molecules
  SET SMILES = 'Nc1ccc(cc1)C(=O)O'
WHERE MoleculeUpacName = '4-Aminobenzoic Acid';

-- 37. 2,4-Dihydroxybenzoic Acid
UPDATE cheminf3_molecules
  SET SMILES = 'O=C(O)c1c(O)ccc(O)c1'
WHERE MoleculeUpacName = '2,4-Dihydroxybenzoic Acid';

-- 38. 3-Acetylsalicylic Acid 
-- (here, the acetyl group is directly bonded to the aromatic ring rather than as an ester)
UPDATE cheminf3_molecules
  SET SMILES = 'O=C(O)c1c(O)c(C(=O)C)cccc1'
WHERE MoleculeUpacName = '3-Acetylsalicylic Acid';

-- 39. Phenol
UPDATE cheminf3_molecules
  SET SMILES = 'Oc1ccccc1'
WHERE MoleculeUpacName = 'Phenol';

-- 40. Aniline
UPDATE cheminf3_molecules
  SET SMILES = 'Nc1ccccc1'
WHERE MoleculeUpacName = 'Aniline';
