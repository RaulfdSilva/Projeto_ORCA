import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_connection():
    """Retorna uma conexão com o banco de dados com timeout para evitar 'database is locked'."""
    return sqlite3.connect("usuarios.db", timeout=10)

def init_db():
    """Inicializa a tabela de usuários com todos os campos necessários para o projeto ORCA."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
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
        print("Banco de dados inicializado com sucesso!")
    finally:
        conn.close()

def cadastrar_usuario_completo(nome, sobrenome, email, username, password, codigo):
    """Realiza o hash da senha e insere o novo usuário como inativo (is_active=0)."""
    conn = get_connection()
    try:
        hashed_password = pwd_context.hash(password)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (nome, sobrenome, email, username, password, codigo_verificacao, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (nome, sobrenome, email, username, hashed_password, codigo))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade (Usuário/Email já existe): {e}")
        return False
    except Exception as e:
        print(f"Erro real no banco de dados: {e}")
        return False
    finally:
        conn.close()

def confirmar_codigo(email, codigo_digitado):
    """Verifica o código de 6 dígitos e ativa a conta do usuário."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ? AND codigo_verificacao = ?", (email, codigo_digitado))
        user = cursor.fetchone()
        
        if user:
            cursor.execute("UPDATE users SET is_active = 1, codigo_verificacao = NULL WHERE email = ?", (email,))
            conn.commit()
            return True
        return False
    finally:
        conn.close()

def verificar_login(username, password):
    """Valida as credenciais e verifica se a conta foi ativada via e-mail."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password, is_active FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result:
            db_password, is_active = result
            if pwd_context.verify(password, db_password):
                if is_active == 1:
                    return {"status": "sucesso", "mensagem": "Login realizado"}
                return {"status": "pendente", "mensagem": "Conta não ativada via e-mail"}
        
        return {"status": "erro", "mensagem": "Usuário ou senha incorretos"}
    finally:
        conn.close()