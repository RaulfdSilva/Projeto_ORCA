from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import auth
import random
from email_service import enviar_email_verificacao

app = FastAPI(title="ORCA System API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth.init_db()

@app.get("/")
def read_root():
    return {"status": "Online", "system": "ORCA"}

@app.post("/cadastro")
def register(
    nome: str = Form(...), 
    sobrenome: str = Form(...), 
    email: str = Form(...), 
    username: str = Form(...), 
    password: str = Form(...),
    password_confirm: str = Form(...)
):
    if password != password_confirm:
        raise HTTPException(status_code=400, detail="As senhas não coincidem")

    codigo = str(random.randint(100000, 999999))
    
    sucesso = auth.cadastrar_usuario_completo(nome, sobrenome, email, username, password, codigo)
    
    if sucesso:
        enviou = enviar_email_verificacao(email, codigo)
        if enviou:
            return {"message": "Código enviado! Verifique sua caixa de entrada."}
        else:
            print(f"ALERTA: Falha no SMTP. Código de backup: {codigo}")
            return {"message": "Cadastro realizado, mas houve erro no envio do e-mail."}

    raise HTTPException(status_code=400, detail="Usuário ou E-mail já existem")

@app.post("/verificar-codigo")
def verificar(email: str = Form(...), codigo: str = Form(...)):
    if auth.confirmar_codigo(email, codigo):
        return {"message": "Conta ativada com sucesso!"}
    
    raise HTTPException(status_code=400, detail="Código inválido ou expirado")

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    resultado = auth.verificar_login(username, password)
    
    if resultado["status"] == "sucesso":
        return {
            "message": "Login realizado!",
            "user": username,
            "redirect": "/dashboard"
        }
    
    elif resultado["status"] == "pendente":
        raise HTTPException(status_code=403, detail=resultado["mensagem"])
    
    else:
        raise HTTPException(status_code=401, detail=resultado["mensagem"])