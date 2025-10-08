import sqlite3
import bcrypt

# Cria o banco e a tabela
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    nivel TEXT NOT NULL
)
''')

# Cria um usuário admin inicial
senha = b"admin123"
senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt())

cursor.execute('''
INSERT OR IGNORE INTO usuarios (nome, usuario, senha_hash, nivel)
VALUES (?, ?, ?, ?)
''', ("Isabella Pereira", "isa", senha_hash, "admin"))

conn.commit()
conn.close()
print("✅ Banco de usuários criado com sucesso!")
