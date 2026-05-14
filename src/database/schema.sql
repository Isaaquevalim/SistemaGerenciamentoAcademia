-- schema.sql
-- define a estrutura do banco de dados da academia
-- tabela de planos disponiveis na academia

-- Tabela de planos disponiveis
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- id gerado automaticamente
    nome TEXT NOT NULL,   -- ex: Mensal, Trimestral, Anual
    preco REAL NOT NULL   -- valor em reais do plano
);

-- tabela principal de alunos
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,  -- cpf unico, alunos nao podem compartilhar cpf
    telefone TEXT,
    email TEXT NOT NULL UNIQUE, -- email unico, alunos nao podem compartilhar email
    status TEXT NOT NULL DEFAULT 'ativo', --'ativo' ou 'inativo
    plano_id INTEGER, 
    FOREIGN KEY (plano_id) REFERENCES planos(id) -- liga o aluno a um plano
);

-- aulas oferecidas pela academia
CREATE TABLE IF NOT EXISTS aulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- id gerado automaticamente
    nome TEXT NOT NULL, -- ex: Yoga, Musculação, Zumba
    horario TEXT NOT NULL, -- horario da aula, ex: "Segunda 18:00", "Quarta 19:00"
    professor TEXT NOT NULL, -- professor que ministra a aula
    vagas_totais INTEGER NOT NULL, -- total de vagas para a aula
    vagas_disponiveis INTEGER NOT NULL -- decrementado ao inscrever alunos
);

-- planos padrao da academia
-- INSERT OR IGNORE: so insere se ainda nao existir um plano com o mesmo id, evita duplicatas ao reiniciar
INSERT OR IGNORE INTO planos (id, nome, preco) VALUES (1, 'Mensal', 99.90);
INSERT OR IGNORE INTO planos (id, nome, preco) VALUES (2, 'Trimestral', 269.90);
INSERT OR IGNORE INTO planos (id, nome, preco) VALUES (3, 'Anual', 899.90);

-- dados iniciais de aulas exemplo
INSERT OR IGNORE INTO aulas (id, nome, horario, professor, vagas_totais, vagas_disponiveis) 
VALUES (1, 'Spinning', '07:00', 'Spinning', 15, 15);
INSERT OR IGNORE INTO aulas (id, nome, horario, professor, vagas_totais, vagas_disponiveis) 
VALUES (2, 'Yoga', '9:00', 'Ana', 20, 20);
INSERT OR IGNORE INTO aulas (id, nome, horario, professor, vagas_totais, vagas_disponiveis) 
VALUES (3, 'Muay Thai', '19:00', 'Roberto', 12, 12);
INSERT OR IGNORE INTO aulas (id, nome, horario, professor, vagas_totais, vagas_disponiveis) 
VALUES (4, 'Pilates', '10:00', 'Fernanda', 10, 10);
