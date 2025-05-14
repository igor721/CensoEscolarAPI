from marshmallow import Schema, fields, validate


class InstituicaoEnsino():
    def __init__(self, id, no_entidade, co_entidade, qt_mat_bas):
        self.id = id
        self.no_entidade = no_entidade
        self.co_entidade = co_entidade
        self.qt_mat_bas = qt_mat_bas

    def toDict(self):
        return {"id": self.id, "no_entidade": self.no_entidade, "co_entidade": self.co_entidade, "qt_mat_bas": self.qt_mat_bas}


class InstituicaoEnsinoSchema(Schema):
    no_entidade = fields.String(validate=validate.Length(min=2, max=100),
                                required=True, error_messages={"required": "Nome da Entidade é obrigatório."})
    co_entidade = fields.Integer(required=True, error_messages={
                                 "required": "Nome da Entidade é obrigatório."})
    qt_mat_bas = fields.Integer(required=True, error_messages={
        "required": "Nome da Entidade é obrigatório."})
