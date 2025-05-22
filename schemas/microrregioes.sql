DROP TABLE IF EXISTS tb_microrregiao;

CREATE TABLE IF NOT EXISTS tb_microrregiao (
    co_microrregiao INTEGER PRIMARY KEY,
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
