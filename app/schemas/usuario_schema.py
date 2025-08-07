from .. import ma
from marshmallow import fields, validate
from ..models.usuario import Usuario

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = False
        fields = ("id", "nome", "email", "senha", "perfil" )
    id = fields.Int(dump_only=True)
    nome= fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    senha= fields.Str(required=True, load_only=True, validate=[
        validate.Length(min=6),  # tamanho mínimo
        validate.Regexp(
    r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).+$',
    error="A senha deve conter ao menos uma letra maiúscula, uma minúscula, um número e um símbolo.")
    ])
    perfil = fields.Str()