from fastapi import FastAPI, HTTPException, Form
import pandas as pd
from binance.client import Client
from sklearn.linear_model import LinearRegression
import numpy as np
import auth 
import random

app = FastAPI(title="Crypto AI Predictor API")

auth.init_db()
client = Client()

# --- FUNÇÕES AUXILIARES ---

def get_historical_data(symbol: str):
    klines = client.get_historical_klines(symbol.upper(), "1m", "2 hours")
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'
    ])
    df = df[['close']].astype(float)
    return df

def train_and_predict(df):
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['close'].values
    model = LinearRegression().fit(X, y)
    previsao = model.predict([[len(df) + 60]])
    return float(previsao[0])

# --- ROTAS DE AUTENTICAÇÃO ---

@app.post("/cadastro")
def register(
    nome: str = Form(...), 
    sobrenome: str = Form(...),
    email: str = Form(...),
    username: str = Form(...), 
    password: str = Form(...),
    password_confirm: str = Form(...)  
):
    # Note que agora o 'if' está alinhado dentro da função
    if password != password_confirm:
        raise HTTPException(status_code=400, detail="As senhas não coincidem")

    if "@" not in email:
        raise HTTPException(status_code=400, detail="E-mail inválido")

    codigo = str(random.randint(100000, 999999))
    
    sucesso = auth.cadastrar_usuario_completo(nome, sobrenome, email, username, password, codigo)
    
    if sucesso:
        print(f"DEBUG: Código para {email} é {codigo}") 
        return {"message": "Usuário pré-cadastrado! Verifique seu e-mail."}
    
    raise HTTPException(status_code=400, detail="Usuário ou E-mail já existem")

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if auth.verificar_usuario(username, password):
        return {"status": "Login aprovado", "user": username}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# --- ROTAS DE DADOS ---

@app.get("/previsao/{symbol}")
def predict_price(symbol: str):
    try:
        dados = get_historical_data(symbol)
        atual = dados['close'].iloc[-1]
        previsao = train_and_predict(dados)
        
        return {
            "moeda": symbol.upper(),
            "preco_atual": round(atual, 4),
            "previsao_1h": round(previsao, 4),
            "tendencia": "ALTA" if previsao > atual else "BAIXA"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "Online"}