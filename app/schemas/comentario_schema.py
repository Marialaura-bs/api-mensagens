from .. import ma
from marshmallow import fields, validate
from ..models.comentario import Comentario

class ComentarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comentario
        load_instance = False #permite o desempacotamento do dicionário no comment_controller.criar_comentario
        fields = ("id", "usuario_id", "mensagem_id", "conteudo", "data_criacao")
    id = fields.Int(dump_only=True)
    usuario_id = fields.Int(dump_only=True)
    mensagem_id = fields.Int(dump_only=True)  # <- alterado aqui
    conteudo = fields.Str(required=True, validate=validate.Length(min=1))
    data_criacao = fields.DateTime(dump_only=True)