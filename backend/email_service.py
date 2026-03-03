import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMETENTE = "orca.email.shooter@gmail.com"
SENHA_REMETENTE = "phtp ebpg fjdq ndrg" 

def enviar_email_verificacao(email_destino, codigo):
    msg = MIMEMultipart()
    msg['From'] = f"Sistema ORCA <{EMAIL_REMETENTE}>"
    msg['To'] = email_destino
    msg['Subject'] = f"Seu Código de Ativação ORCA: {codigo}"

    corpo = f"""
    <div style="font-family: sans-serif; background-color: #0b0e11; color: white; padding: 40px; border-radius: 15px; text-align: center;">
        <h1 style="color: #f0b90b;">ORCA SYSTEM</h1>
        <p style="color: #b7bdc6; font-size: 16px;">Olá! Use o código abaixo para validar seu cadastro:</p>
        <div style="background-color: #1e2329; padding: 20px; font-size: 36px; font-weight: bold; border: 2px solid #f0b90b; border-radius: 10px; color: #f0b90b; letter-spacing: 10px; display: inline-block; margin: 25px 0;">
            {codigo}
        </div>
        <p style="font-size: 12px; color: #848e9c;">Se você não solicitou este e-mail, pode ignorá-lo com segurança.</p>
    </div>
    """
    msg.attach(MIMEText(corpo, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        server.sendmail(EMAIL_REMETENTE, email_destino, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"ERRO SMTP: {e}")
        return False