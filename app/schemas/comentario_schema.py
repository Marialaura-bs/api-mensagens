from .. import ma
from marshmallow import fields, validate
from ..models.comentario import Comentario
from .usuario_schema import UsuarioSchema

class ComentarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comentario
        load_instance = False #permite o desempacotamento do dicionário no comment_controller.criar_comentario
        fields = ("id", "autor", "mensagem", "content", "created_at")
    id = fields.Int(dump_only=True)
    autor = fields.Nested(UsuarioSchema, dump_only=True)
    mensagem = fields.Int(dump_only=True)  # <- alterado aqui
    content = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)