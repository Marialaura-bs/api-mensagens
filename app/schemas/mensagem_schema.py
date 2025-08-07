from .. import ma
from marshmallow import fields, validate
from ..models.mensagem import Mensagem

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mensagem
        load_instance = True  
        fields = ("id", "titulo", "conteudo", "usuario_id", "data_criacao")  # mantém a ordem do modelo
    id = fields.Int(dump_only=True)
    titulo=fields.Str(required=True, validate=validate.Length(min=1))
    conteudo = fields.Str(required=True, validate=validate.Length(min=1))
    usuario_id = fields.Int(load_only=True)
    data_criacao = fields.DateTime(dump_only=True)