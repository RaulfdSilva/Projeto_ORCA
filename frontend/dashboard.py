import streamlit as st
import requests


st.set_page_config(page_title="Crypto AI", layout="wide")
API_URL = "http://127.0.0.1:8000"

if 'logado' not in st.session_state:
    st.session_state.logado = False

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
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome")
            sobrenome = col2.text_input("Sobrenome")
    
            email = st.text_input("E-mail")
            new_user = st.text_input("Escolha um Usuário")
            
            col3, col4 = st.columns(2)
            new_pw = col3.text_input("Senha", type="password")
            confirm_pw = col4.text_input("Repita a Senha", type="password")
            register_btn = st.form_submit_button("Criar Conta")
            
            if register_btn:

                dados = {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "username": new_user,
                    "password": new_pw,
                    "password_confirm": confirm_pw 
                }
                try:
                    res = requests.post(
                        f"{API_URL}/cadastro", 
                        data=dados,
                        timeout=5
                    )
                    if res.status_code == 200:
                        st.success("✅ Conta criada! Agora vá na aba 'Entrar'.")
                    else:
                        st.error(f"Erro: {res.json().get('detail', 'Usuário já existe')}")
                except Exception as e:
                    st.error(f"Erro ao conectar: {e}")

else:
    st.sidebar.write(f"Conectado como: **{st.session_state.username}**")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()
    
    st.title(f"Bem-vindo, {st.session_state.username}!")
    st.write("O sistema de IA está pronto para análise.")
    # Aqui continuaria o restante do seu código de análise...