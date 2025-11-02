#!/usr/bin/env python3 

from flask import Flask, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # clé secrète pour session

# ----- Configuration OIDC / Keycloak -----
KEYCLOAK_SERVER = "http://cloaky:8080/auth"
REALM = "xencloak"
CLIENT_ID = "xencloak"
CLIENT_SECRET = "79be32ee-9058-4170-8fb4-eefd6e999c4d"  # ou None pour public client
REDIRECT_URI = "http://localhost:7777/auth/callback"

oauth = OAuth(app)
keycloak = oauth.register(
    name='keycloak',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{KEYCLOAK_SERVER}/realms/{REALM}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'}
)

# ----- Routes -----

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f"Hello {user['preferred_username']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login with Keycloak</a>"

@app.route('/login')
def login():
    redirect_uri = REDIRECT_URI
    # génère un nonce et le stocke dans la session
    nonce = os.urandom(16).hex()
    session['nonce'] = nonce
    return keycloak.authorize_redirect(redirect_uri=redirect_uri, nonce=nonce)

@app.route('/auth/callback')
def auth_callback():
    token = keycloak.authorize_access_token()
    # on passe le nonce stocké dans la session
    user = keycloak.parse_id_token(token, nonce=session.get('nonce'))
    session['user'] = user
    session['token'] = token
    return redirect('/')

@app.route('/protected')
def protected():
    if 'user' not in session:
        return redirect(url_for('login'))
    return jsonify({
        "msg": "This is a protected route",
        "user": session['user']
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(f"{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/logout?redirect_uri=http://localhost:7777/")

# ----- Run -----
if __name__ == '__main__':
    app.run(debug=True, port=7777)

