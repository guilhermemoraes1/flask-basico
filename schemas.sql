DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE tb_instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no_regiao TEXT NOT NULL,
    co_regiao INTEGER NOT NULL,
    no_uf TEXT NOT NULL,
    sg_uf TEXT NOT NULL,
    co_uf INTEGER NOT NULL,
    no_entidade TEXT NOT NULL,
    co_entidade INTEGER NOT NULL,
    no_municipio TEXT NOT NULL,
    co_municipio INTEGER NOT NULL,
    no_mesorregiao TEXT NOT NULL,
    co_mesorregiao INTEGER NOT NULL,
    no_microrregiao TEXT NOT NULL,
    co_microrregiao INTEGER NOT NULL,
    qt_mat_bas INTEGER,
    qt_mat_inf INTEGER,
    qt_mat_fund INTEGER,
    qt_mat_med INTEGER,
    qt_mat_eja INTEGER,
    qt_mat_esp INTEGER
);
