from app import create_app
from models import Base
from sqlalchemy import create_engine
import os

# Cria o diretório de banco de dados se não existir
os.makedirs('instance', exist_ok=True)

# Cria o banco de dados
app = create_app()
with app.app_context():
    engine = create_engine('sqlite:///instance/tour4friends.db')
    Base.metadata.create_all(engine)
    print("Banco de dados criado com sucesso em: instance/tour4friends.db")
