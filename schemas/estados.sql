DROP TABLE IF EXISTS tb_estado;

CREATE TABLE IF NOT EXISTS tb_estado (
    co_uf INTEGER PRIMARY KEY,
    sg_uf TEXT,
    no_uf TEXT,
    co_regiao INTEGER,
    sg_regiao TEXT,
    no_regiao TEXT
);