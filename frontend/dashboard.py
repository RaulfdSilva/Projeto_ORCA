import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Crypto AI", layout="wide")
API_URL = "http://127.0.0.1:8000"

# Inicializa o estado de login se não existir
if 'logado' not in st.session_state:
    st.session_state.logado = False

# --- INTERFACE DE LOGIN ---
if not st.session_state.logado:
    st.title("🔐 Acesso ao Sistema")
    
    tab1, tab2 = st.tabs(["Entrar", "Criar Conta"])
    
    with tab1:
        with st.form("form_login"):
            user = st.text_input("Usuário")
            pw = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                try:
                    # Enviando como Form Data para o FastAPI
                    res = requests.post(
                        f"{API_URL}/login", 
                        data={"username": user, "password": pw},
                        timeout=5
                    )
                    
                    if res.status_code == 200:
                        st.session_state.logado = True
                        st.session_state.username = user
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {res.json().get('detail', 'Credenciais inválidas')}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Erro de Conexão: O Backend (main.py) está rodando?")

    with tab2:
        with st.form("form_registro"):
            new_user = st.text_input("Escolha um Usuário")
            new_pw = st.text_input("Escolha uma Senha", type="password")
            register_btn = st.form_submit_button("Cadastrar")
            
            if register_btn:
                try:
                    res = requests.post(
                        f"{API_URL}/cadastro", 
                        data={"username": new_user, "password": new_pw},
                        timeout=5
                    )
                    if res.status_code == 200:
                        st.success("✅ Conta criada! Agora vá na aba 'Entrar'.")
                    else:
                        st.error(f"Erro: {res.json().get('detail', 'Usuário já existe')}")
                except Exception as e:
                    st.error(f"Erro ao conectar: {e}")

# --- TELA PRINCIPAL (PÓS-LOGIN) ---
else:
    st.sidebar.write(f"Conectado como: **{st.session_state.username}**")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()
    
    st.title(f"Bem-vindo, {st.session_state.username}!")
    st.write("O sistema de IA está pronto para análise.")
    # Aqui continuaria o restante do seu código de análise...