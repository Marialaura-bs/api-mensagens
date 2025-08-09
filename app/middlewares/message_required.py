from flask import request, abort
from functools import wraps
from ..controllers import message_controller

def mensagem_existe(f):
    @wraps(f)
    def decorated_function(mensagem_id, *args, **kwargs):
        message = message_controller.obter_mensagem(mensagem_id)
        if message is None:
            abort(404, description="Mensagem não encontrada.")
        request.mensagem = message
        return f(mensagem_id, *args, **kwargs)
    return decorated_function
