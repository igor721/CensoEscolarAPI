CREATE TABLE IF NOT EXISTS instituicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codEntidade INTEGER UNIQUE NOT NULL,
    entidade TEXT NOT NULL,
    regiao TEXT,
    uf TEXT,
    municipio TEXT,
    mesoregiao TEXT,
    microregiao TEXT,
    matriculas_base INTEGER
);