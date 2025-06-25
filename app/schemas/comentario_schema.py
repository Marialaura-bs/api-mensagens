from .. import ma
from marshmallow import fields, validate
from ..models.comentario import Comentario

class ComentarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comentario
        load_instance = True  
        fields = ("id", "autor", "mensagem", "content", "created_at")
    id = fields.Int(dump_only=True)
    autor = fields.Int(dump_only=True)
    mensagem = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)