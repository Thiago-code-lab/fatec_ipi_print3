from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

from models import User, Itinerary, Day, POI

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/login')
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'error': 'Credenciais inválidas'}), 400

    session = current_app.session()
    user = session.execute(select(User).where(User.email == email)).scalars().first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return jsonify({'error': 'Email ou senha incorretos'}), 401

    token = create_access_token(identity={"id": user.id, "email": user.email, "name": user.name})
    return jsonify({'access_token': token, 'user': {'id': user.id, 'email': user.email, 'name': user.name}})

@auth_bp.post('/register')
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not name or not email or not password:
        return jsonify({'error': 'Dados incompletos'}), 400

    session = current_app.session()
    exists = session.execute(select(User).where(User.email == email)).scalars().first()
    if exists:
        return jsonify({'error': 'Email já cadastrado'}), 409

    user = User(name=name, email=email, password_hash=bcrypt.hash(password))
    session.add(user)
    session.commit()

    # Create basic itinerary scaffold
    itinerary = Itinerary(user_id=user.id, title='Caminho de Santiago - Roteiro Padrão', description='Roteiro personalizado pela Tour4Friends')
    session.add(itinerary)
    session.commit()

    token = create_access_token(identity={"id": user.id, "email": user.email, "name": user.name})
    return jsonify({'access_token': token, 'user': {'id': user.id, 'email': user.email, 'name': user.name}}), 201

@auth_bp.post('/seed-demo')
def seed_demo():
    """Seeds a demo user with a small itinerary for beta testing."""
    session = current_app.session()

    email = 'peregrino@tour4friends.com'
    user = session.execute(select(User).where(User.email == email)).scalars().first()
    if not user:
        user = User(name='Peregrino Demo', email=email, password_hash=bcrypt.hash('senha123'))
        session.add(user)
        session.commit()

    itinerary = session.execute(select(Itinerary).where(Itinerary.user_id == user.id)).scalars().first()
    if not itinerary:
        itinerary = Itinerary(user_id=user.id, title='Caminho de Santiago - Demo', description='Itinerário de demonstração')
        session.add(itinerary)
        session.commit()

        day1 = Day(
            itinerary_id=itinerary.id,
            day_number=1,
            date="",
            start_location='Saint-Jean-Pied-de-Port',
            end_location='Roncesvalles',
            distance_km=24.0,
            lodging_info='Albergue de Roncesvalles',
            notes='Subida forte nos Pirineus. Leve água.',
            polyline='[{"lat":43.1631, "lng":-1.2376}, {"lat":43.0090, "lng":-1.3213}]'
        )
        session.add(day1)
        session.commit()

        pois = [
            POI(day_id=day1.id, name='Mirante Pirineus', description='Vista incrível das montanhas.', category='paisagem', lat=43.09, lng=-1.29),
            POI(day_id=day1.id, name='Restaurante Basco', description='Culinária local.', category='restaurante', lat=43.05, lng=-1.30),
        ]
        session.add_all(pois)
        session.commit()

    return jsonify({'ok': True})
