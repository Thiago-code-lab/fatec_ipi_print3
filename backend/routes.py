import json
from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select

from models import User, Itinerary, Day, POI

api_bp = Blueprint('api', __name__)

@api_bp.get('/me/itinerary')
@jwt_required()
def get_my_itinerary():
    identity = get_jwt_identity() or {}
    user_id = identity.get('id')
    session = current_app.session()

    itinerary = session.execute(select(Itinerary).where(Itinerary.user_id == user_id)).scalars().first()
    if not itinerary:
        return jsonify({'itinerary': None})

    def day_to_dict(d: Day):
        return {
            'id': d.id,
            'day_number': d.day_number,
            'date': d.date,
            'start_location': d.start_location,
            'end_location': d.end_location,
            'distance_km': d.distance_km,
            'lodging_info': d.lodging_info,
            'notes': d.notes,
        }

    data = {
        'id': itinerary.id,
        'title': itinerary.title,
        'description': itinerary.description,
        'days': [day_to_dict(d) for d in sorted(itinerary.days, key=lambda x: x.day_number)]
    }
    return jsonify({'itinerary': data})

@api_bp.get('/days/<int:day_id>/map')
@jwt_required()
def get_day_map(day_id: int):
    session = current_app.session()
    day = session.execute(select(Day).where(Day.id == day_id)).scalars().first()
    if not day:
        return jsonify({'error': 'Dia não encontrado'}), 404

    pois = session.execute(select(POI).where(POI.day_id == day_id)).scalars().all()

    try:
        polyline = json.loads(day.polyline) if day.polyline else []
    except Exception:
        polyline = []

    return jsonify({
        'day': {
            'id': day.id,
            'start_location': day.start_location,
            'end_location': day.end_location,
        },
        'route': polyline,
        'pois': [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'category': p.category,
                'lat': p.lat,
                'lng': p.lng,
            } for p in pois
        ]
    })
