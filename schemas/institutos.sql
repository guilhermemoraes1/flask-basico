DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE IF NOT EXISTS tb_instituicao (
    id SERIAL PRIMARY KEY,
    co_regiao INTEGER,
    no_regiao TEXT,
    co_uf INTEGER,
    sg_uf TEXT,
    no_uf TEXT,
    co_municipio INTEGER,
    no_municipio TEXT,
    co_mesorregiao INTEGER,
    no_mesorregiao TEXT,
    co_microrregiao INTEGER,
    no_microrregiao TEXT,
    no_entidade TEXT,
    co_entidade TEXT,
    qt_mat_bas INTEGER,
    qt_mat_inf INTEGER,
    qt_mat_fund INTEGER,
    qt_mat_med INTEGER,
    qt_mat_eja INTEGER,
    qt_mat_esp INTEGER
);