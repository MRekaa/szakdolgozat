CREATE DATABASE labor;

CREATE TABLE materials (
    name VARCHAR(255)
);

CREATE TABLE reactions (
    item1 VARCHAR(255)
    item2 VARCHAR(255)
    result text
    equation VARCHAR(255)
    type VARCHAR(50)
);

CREATE TABLE tools (
    name VARCHAR(255)
);

INSERT INTO materials (name) VALUES
('Al'),
('C'),
('Cl2'),
('F2'),
('H2'),
('H2O'),
('He'),
('I2'),
('KMnO4'),
('Mg'),
('N2'),
('Na'),
('O2'),
('O3'),
('S');

INSERT INTO tools (name) VALUES
('Bunsen'),
('Cooler'),
('Distiller'),
('Electricity'),
('Pipetta'),
('Tap water');

INSERT INTO reactions (item1, item2, result, equation, type) VALUES
('H2', 'O2', '["H2O"]', '2H2 + O2 -> 2H2O', 'material'),
('H2', 'Cl2', '["HCl"]', 'H2 + Cl2 -> 2HCl', 'material'),
('H2O', 'CO2', '["H2CO3"]', 'H2O + CO2 -> H2CO3', 'material'),
('Na', 'Cl2', '["NaCl"]', '2Na + Cl2 -> 2NaCl', 'material'),
('N2', 'H2', '["NH3"]', 'N2 + 3H2 -> 2NH3', 'material'),
('C', 'O2', '["CO2"]', 'C + O2 -> CO2', 'material'),
('C', 'CO2', '["CO"]', 'C + CO2 -> 2CO', 'material'),
('I2', NULL, '["Al+I2"]', NULL, 'material'),
('H2', 'F2', '["HF"]', 'H2 + F2 -> 2HF', 'material'),
('Al+I2', 'Pipetta(H2O)', '["AlI3"]', '2Al + 3I2 -> 2AlI3', 'material'),
('C+O2', 'Bunsen', 'CO2', NULL, 'material'),
('H2O', 'Electricity', '["H2","O2"]', '2H2O -> 2H2 + O2', 'material'),
('H2O', 'Pipetta', 'Pipetta(H2O)', NULL, 'material'),
('KMnO4', 'Bunsen', '["K2MnO4+MnO4","O2"]', '2KMnO4 -> K2MnO4 + MnO2 + O2', 'material'),
('H2O', 'Cooler', 'H2O(Cooled)', NULL, 'material'),
('Tap water', 'Distiller', 'H2O', NULL, 'material');