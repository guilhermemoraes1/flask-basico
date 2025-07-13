from marshmallow import Schema, fields, validate

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

class InstituicaoSchema(Schema):
    no_regiao = fields.Str(required=True, error_messages={"required": "Informe o nome da região."})
    co_regiao = fields.Int(required=True, error_messages={"required": "Informe o código da região."})
    sg_uf = fields.Str(required=True, error_messages={"required": "Informe a sigla da UF."})
    co_uf = fields.Int(required=True, error_messages={"required": "Informe o código da UF."})
    no_entidade = fields.Str(required=True, error_messages={"required": "Informe o nome da entidade."})
    co_entidade = fields.Int(required=True, error_messages={"required": "Informe o código da entidade."})
    co_municipio = fields.Int(required=True, error_messages={"required": "Informe o código do município."})
    co_mesorregiao = fields.Int(required=True, error_messages={"required": "Informe o código da mesorregião."})
    co_microrregiao = fields.Int(required=True, error_messages={"required": "Informe o código da microrregião."})
    qt_mat_bas = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para educação básica."})
    qt_mat_inf = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para educação infantil."})
    qt_mat_fund = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para ensino fundamental."})
    qt_mat_med = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para ensino médio."})
    qt_mat_eja = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para EJA."})
    qt_mat_esp = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para educação especial."})

