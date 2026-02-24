import sqlite3
from passlib.context import CryptContext

# Configuração de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    # Criando a tabela com as novas colunas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            sobrenome TEXT,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            password TEXT,
            is_active INTEGER DEFAULT 0,
            codigo_verificacao TEXT
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_usuario_completo(nome, sobrenome, email, username, password, codigo):
    try:
        hashed = pwd_context.hash(password)
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (nome, sobrenome, email, username, password, codigo_verificacao, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (nome, sobrenome, email, username, hashed, codigo))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro no banco de dados: {e}")
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