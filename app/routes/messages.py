from flask import Blueprint, jsonify
from app.models.message import Message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route("/", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([msg.to_dict() for msg in messages])