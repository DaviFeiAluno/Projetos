import sqlite3

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS producao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maquina TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    data TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

cursor.execute(
    "INSERT OR IGNORE INTO usuarios (username, senha) VALUES (?, ?)",
    ("admin", "1234")
)

conn.commit()
conn.close()

print("Banco e tabelas criados com sucesso!")