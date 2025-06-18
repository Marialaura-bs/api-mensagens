from .. import ma
from marshmallow import fields, validate
from ..models.usuario import Usuario

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True  
        fields = ("id", "email", "nome", "senha" )
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    nome= fields.Str(required=True, validate=validate.Length(min=1))
    senha= fields.Str(required=True, validate=[
            validate.Length(min=8),  # tamanho mínimo
            validate.Regexp( r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@!%*?&]).+$')
    ])