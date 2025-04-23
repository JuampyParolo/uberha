from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("UBER_CLIENT_ID")
CLIENT_SECRET = os.getenv("UBER_CLIENT_SECRET")
REDIRECT_URI = os.getenv("UBER_REDIRECT_URI", "https://uberha.onrender.com/callback")

@app.route("/")
def index():
    auth_url = (
        f"https://login.uber.com/oauth/v2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&scope=profile"
        f"&redirect_uri={REDIRECT_URI}"
    )
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

    response = requests.post(token_url, data=data)
    return response.json()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

