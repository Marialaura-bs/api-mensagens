from .. import ma
from marshmallow import fields, validate
from ..models.mensagem import Mensagem
from .comentario_schema import ComentarioSchema

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mensagem
        load_instance = False  
        fields = ("id", "titulo", "conteudo", "usuario_id", "data_criacao")  # mantém a ordem do modelo
    id = fields.Int(dump_only=True)
    titulo=fields.Str(required=True, validate=validate.Length(min=1))
    conteudo = fields.Str(required=True, validate=validate.Length(min=1))
    usuario_id = fields.Int(dump_only=True)
    data_criacao = fields.DateTime(dump_only=True)

    # Campo aninhado de comentários
    comentario = fields.Nested(ComentarioSchema, many=True, dump_only=True)