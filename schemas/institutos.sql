DROP TABLE IF EXISTS tb_instituicao;


CREATE TABLE IF NOT EXISTS tb_instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    co_regiao TEXT,
    no_regiao TEXT,
    co_uf TEXT,
    sg_uf TEXT,
    no_uf TEXT,
    co_municipio TEXT,
    no_municipio TEXT,
    co_mesorregiao TEXT,
    no_mesorregiao TEXT,
    co_microrregiao TEXT,
    no_microrregiao TEXT,
    no_entidade TEXT,
    co_entidade TEXT,
    qt_mat_bas INTEGER,
    qt_mat_inf INTEGER,
    qt_mat_fund INTEGER,
    qt_mat_med INTEGER,
    qt_mat_eja INTEGER,
    qt_mat_esp INTEGER,
    FOREIGN KEY (co_uf) REFERENCES tb_municipio(co_uf),
    FOREIGN KEY (co_municipio) REFERENCES tb_municipio(co_municipio),
    FOREIGN KEY (co_mesorregiao) REFERENCES tb_municipio(co_mesorregiao),
    FOREIGN KEY (co_microrregiao) REFERENCES tb_municipio(co_microrregiao)
);
