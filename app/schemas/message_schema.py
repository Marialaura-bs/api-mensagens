from .. import ma
from marshmallow import fields, validate
from ..models.message import Message
from .usuario_schema import UsuarioSchema

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True  
        fields = ("id", "autor", "content", "created_at")  # mantém a ordem do modelo
    id = fields.Int(dump_only=True)
    autor = fields.Nested(UsuarioSchema, dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)