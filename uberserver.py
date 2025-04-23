from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("sFksMuO06Q_g6XGayHtixwegmCAPjBl4")
CLIENT_SECRET = os.getenv("_njo4RLJS0E2jNU9ImLzlsBMirjTrJH8FNOqqXS_")
REDIRECT_URI = os.getenv("UBER_REDIRECT_URI", "https://<TU_DOMINIO>.onrender.com/callback")

@app.route("/")
def index():
    auth_url = f"https://login.uber.com/oauth/v2/authorize?client_id={CLIENT_ID}&response_type=code&scope=profile&redirect_uri={REDIRECT_URI}"
    return f'<a href="{auth_url}">Iniciar sesión con Uber</a>'

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Código no recibido", 400

    token_url = "https://login.uber.com/oauth/v2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    r = requests.post(token_url, data=data)
    return r.json()
