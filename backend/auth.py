import sqlite3
from passlib.context import CryptContext

# Configuração de criptografia
# Mude no auth.py:
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_usuario(username, password):
    try:
        hashed = pwd_context.hash(password)
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def verificar_usuario(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and pwd_context.verify(password, user[0]):
        return True
    return False