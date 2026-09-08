-- Execute no MySQL Workbench ou terminal MySQL 
 
CREATE DATABASE IF NOT EXISTS medicare_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci; 
 -- Seleciona o banco para usar 
USE medicare_db; 

-- Tabela de Planos de Saúde (criamos primeiro pois Paciente depende dela) 
CREATE TABLE IF NOT EXISTS planos ( 
    id       INT AUTO_INCREMENT PRIMARY KEY, 
    nome     VARCHAR(100) NOT NULL, 
    codigo   VARCHAR(20)  NOT NULL, 
    ativo    TINYINT(1)   DEFAULT 1 
); 
 -- Tabela de Médicos 
CREATE TABLE IF NOT EXISTS medicos ( 
    id            INT AUTO_INCREMENT PRIMARY KEY, 
    nome          VARCHAR(100) NOT NULL, 
    especialidade VARCHAR(80)  NOT NULL, 
    crm           VARCHAR(20)  NOT NULL UNIQUE, 
    ativo         TINYINT(1)   DEFAULT 1 
); 
 -- Tabela de Pacientes 
CREATE TABLE IF NOT EXISTS pacientes ( 
    id        INT AUTO_INCREMENT PRIMARY KEY, 
    nome      VARCHAR(100) NOT NULL, 
    cpf       VARCHAR(14)  NOT NULL UNIQUE, 
    telefone  VARCHAR(20), 
    email     VARCHAR(100), 
    plano_id  INT, 
    FOREIGN KEY (plano_id) REFERENCES planos(id) 
); 
 -- Tabela de Agendamentos 
CREATE TABLE IF NOT EXISTS agendamentos ( 
    id          INT AUTO_INCREMENT PRIMARY KEY, 
    paciente_id INT NOT NULL, 
 medico_id   INT NOT NULL, 
    data_hora   DATETIME NOT NULL, 
    status      ENUM('agendado','cancelado','realizado') DEFAULT 
'agendado', 
    observacao  TEXT, 
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id), 
    FOREIGN KEY (medico_id)   REFERENCES medicos(id) 
); 
-- Insira alguns dados para poder testar o sistema 
INSERT INTO planos (nome, codigo) VALUES 
    ('Unimed',      'UNI-001'), 
    ('Bradesco Saúde', 'BRA-002'), 
    ('Particular',  'PAR-000'); 

select * from planos;
INSERT INTO medicos (nome, especialidade, crm) VALUES 
    ('Dr. Carlos Silva',   'Clínico Geral',  'CRM-123456'), 
    ('Dra. Ana Oliveira',  'Cardiologia',    'CRM-789012'), 
    ('Dr. Pedro Santos',   'Ortopedia',      'CRM-345678'); 

select * from medicos;