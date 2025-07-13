DROP TABLE IF EXISTS tb_municipio;

CREATE TABLE IF NOT EXISTS tb_municipio (
    co_municipio INTEGER PRIMARY KEY,
    no_municipio TEXT,
    co_microrregiao INTEGER,
    no_microrregiao TEXT,
    co_mesorregiao INTEGER,
    no_mesorregiao TEXT,
    co_uf INTEGER,
    sg_uf TEXT,
    no_uf TEXT,
    co_regiao INTEGER,
    sg_regiao TEXT,
    no_regiao TEXT
);
