from .. import ma
from marshmallow import fields, validate
from ..models.usuario import Usuario

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True  
        fields = ("id", "email", "nome", "senha", "admin" )
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    nome= fields.Str(required=True, validate=validate.Length(min=2))
    senha= fields.Str(required=True, load_only=True, validate=[
        validate.Length(min=8),  # tamanho mínimo
        validate.Regexp('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@!%*?&]).+$')
    ])
    admin = fields.Bool(dump_only=True)