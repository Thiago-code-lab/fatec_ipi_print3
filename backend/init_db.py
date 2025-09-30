import sqlite3
import os

# Cria o diretório se não existir
os.makedirs('instance', exist_ok=True)

# Conecta ao banco de dados (cria se não existir)
conn = sqlite3.connect('instance/tour4friends.db')
cursor = conn.cursor()

# Cria as tabelas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS itineraries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

print("Banco de dados criado com sucesso em: instance/tour4friends.db")
conn.commit()
conn.close()
