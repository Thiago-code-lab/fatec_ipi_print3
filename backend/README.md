# Tour4Friends Backend (Flask)

## Requisitos
- Python 3.10+

## Setup
1. Crie e ative um virtualenv (opcional).
2. Instale dependências:
```
pip install -r requirements.txt
```
3. Configure variáveis de ambiente copiando `.env.example` para `.env` e ajuste as chaves.
4. Execute (usar eventlet para WebSocket):
```
python app.py
```
5. Opcional: popular dados de demo (usuário: peregrino@tour4friends.com, senha: senha123)
```
curl -X POST http://localhost:5000/api/auth/seed-demo
```

## Endpoints principais
- POST `/api/auth/login` — retorna JWT
- GET `/api/me/itinerary` — requer JWT, retorna roteiro do usuário
- GET `/api/days/<day_id>/map` — requer JWT, rota e POIs do dia
- GET `/api/chat/room` — retorna sala global de suporte
