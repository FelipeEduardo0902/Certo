-- Cria o banco de dados, caso não exista
CREATE DATABASE Teste;

-- Usa o banco de dados criado
USE teste;

-- Cria a tabela curriculos
CREATE TABLE curriculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100) NOT NULL,
    endereco_web VARCHAR(255),
    experiencia TEXT NOT NULL
);
