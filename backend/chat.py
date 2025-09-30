from flask import Blueprint, jsonify, current_app

chat_bp = Blueprint('chat', __name__)

@chat_bp.get('/room')
def get_room():
    return jsonify({'room': current_app.config.get('SUPPORT_ROOM', 'global_support')})
