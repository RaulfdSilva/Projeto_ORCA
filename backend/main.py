from fastapi import FastAPI, HTTPException, Form
import pandas as pd
from binance.client import Client
from sklearn.linear_model import LinearRegression
import numpy as np
import auth  # Importa nosso script de autenticação

app = FastAPI(title="Crypto AI Predictor API")

# Inicializa banco e cliente Binance
auth.init_db()
client = Client()

# --- LÓGICA DE IA ---
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
def register(username: str = Form(...), password: str = Form(...)):
    # Adicionamos uma trava para não aceitar dados vazios
    if not username or not password:
        raise HTTPException(status_code=400, detail="Dados inválidos")
        
    sucesso = auth.cadastrar_usuario(username, password)
    if sucesso:
        return {"message": f"Usuário {username} criado!"}
    raise HTTPException(status_code=400, detail="Usuário já existe")

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