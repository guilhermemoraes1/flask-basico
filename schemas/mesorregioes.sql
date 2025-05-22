DROP TABLE IF EXISTS tb_mesorregiao;

CREATE TABLE IF NOT EXISTS tb_mesorregiao (
    co_mesorregiao INTEGER PRIMARY KEY,
    no_mesorregiao TEXT,
    co_uf INTEGER,
    sg_uf TEXT,
    no_uf TEXT,
    co_regiao INTEGER,
    sg_regiao TEXT,
    no_regiao TEXT
);
