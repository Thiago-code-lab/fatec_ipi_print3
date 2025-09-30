from flask import Flask, jsonify, g, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps
import jwt
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
CORS(app)

# Dados em memória (substituir por banco de dados em produção)
users = {
    "admin@example.com": {
        "password": "senha123",  # Em produção, use hashing de senha
        "name": "Admin",
        "id": 1
    }
}

itinerary = {
    "id": 1,
    "title": "Caminho de Santiago - Roteiro Completo",
    "description": "Roteiro completo do Caminho Francês até Santiago de Compostela",
    "days": [
        {
            "id": 1,
            "day_number": 1,
            "date": "2023-05-01",
            "start_location": "Saint-Jean-Pied-de-Port",
            "end_location": "Roncesvalles",
            "distance_km": 24.0,
            "lodging_info": "Albergue de Roncesvalles",
            "notes": "Subida acentuada nos Pirineus. Leve água e lanche.",
            "polyline": '[{"lat":43.1631, "lng":-1.2376}, {"lat":43.0090, "lng":-1.3213}]',
            "pois": [
                {
                    "id": 1,
                    "name": "Mirante dos Pirineus",
                    "description": "Vista espetacular da cadeia montanhosa",
                    "category": "vista",
                    "lat": 43.09,
                    "lng": -1.29
                }
            ]
        },
        {
            "id": 2,
            "day_number": 2,
            "date": "2023-05-02",
            "start_location": "Roncesvalles",
            "end_location": "Zubiri",
            "distance_km": 21.3,
            "lodging_info": "Albergue Municipal de Zubiri",
            "notes": "Caminhada por florestas e pequenas vilas.",
            "polyline": '[{"lat":43.0090, "lng":-1.3213}, {"lat":42.9307, "lng":-1.5039}]',
            "pois": []
        }
    ]
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token está faltando!'}), 401
        try:
            data = jwt.decode(token.split()[1], app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token inválido!'}), 401
        return f(*args, **kwargs)
    return decorated

# Rotas de autenticação
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400
        
    user = users.get(email)
    if not user or user['password'] != password:
        return jsonify({'message': 'Credenciais inválidas'}), 401
    
    token = jwt.encode({
        'user_id': user['id'],
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=12)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'access_token': token,
        'user': {
            'id': user['id'],
            'email': email,
            'name': user['name']
        }
    })

# Rotas de itinerário
@app.route('/api/itinerary')
@token_required
def get_itinerary():
    return jsonify(itinerary)

@app.route('/api/days/<int:day_id>/map')
@token_required
def get_day_map(day_id):
    day = next((day for day in itinerary['days'] if day['id'] == day_id), None)
    if not day:
        return jsonify({'message': 'Dia não encontrado'}), 404
        
    return jsonify({
        'day': {
            'id': day['id'],
            'start_location': day['start_location'],
            'end_location': day['end_location']
        },
        'route': json.loads(day['polyline']),
        'pois': day.get('pois', [])
    })

# Rota de chat
messages = []

@app.route('/api/chat/messages', methods=['GET', 'POST'])
@token_required
def chat_messages():
    if request.method == 'POST':
        data = request.get_json()
        messages.append({
            'id': len(messages) + 1,
            'text': data.get('text'),
            'sender': 'user',
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Resposta automática
        messages.append({
            'id': len(messages) + 1,
            'text': 'Obrigado pela sua mensagem! Nossa equipe de suporte entrará em contato em breve.',
            'sender': 'support',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
