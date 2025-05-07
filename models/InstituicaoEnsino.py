class InstituicaoEnsino:
    def __init__(
        self, id, no_regiao, co_regiao, no_uf, sg_uf, co_uf,
        no_municipio, co_municipio, no_mesorregiao, co_mesorregiao,
        no_microrregiao, co_microrregiao, no_entidade, co_entidade,
        qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
        qt_mat_eja, qt_mat_esp
    ):
        self.id = id
        self.no_regiao = no_regiao
        self.co_regiao = co_regiao
        self.no_uf = no_uf
        self.sg_uf = sg_uf
        self.co_uf = co_uf
        self.no_municipio = no_municipio
        self.co_municipio = co_municipio
        self.no_mesorregiao = no_mesorregiao
        self.co_mesorregiao = co_mesorregiao
        self.no_microrregiao = no_microrregiao
        self.co_microrregiao = co_microrregiao
        self.no_entidade = no_entidade
        self.co_entidade = co_entidade
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_inf = qt_mat_inf
        self.qt_mat_fund = qt_mat_fund
        self.qt_mat_med = qt_mat_med
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp

    def toDict(self):
        return {
            "id": self.id,
            "no_regiao": self.no_regiao,
            "co_regiao": self.co_regiao,
            "no_uf": self.no_uf,
            "sg_uf": self.sg_uf,
            "co_uf": self.co_uf,
            "no_municipio": self.no_municipio,
            "co_municipio": self.co_municipio,
            "no_mesorregiao": self.no_mesorregiao,
            "co_mesorregiao": self.co_mesorregiao,
            "no_microrregiao": self.no_microrregiao,
            "co_microrregiao": self.co_microrregiao,
            "no_entidade": self.no_entidade,
            "co_entidade": self.co_entidade,
            "qt_mat_bas": self.qt_mat_bas,
            "qt_mat_inf": self.qt_mat_inf,
            "qt_mat_fund": self.qt_mat_fund,
            "qt_mat_med": self.qt_mat_med,
            "qt_mat_eja": self.qt_mat_eja,
            "qt_mat_esp": self.qt_mat_esp
        }
