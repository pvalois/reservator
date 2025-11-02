#!/usr/bin/env python3

import json
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
import os

import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)  # clé secrète pour session

# ----- Configuration OIDC / Keycloak -----
KEYCLOAK_SERVER = "http://cloaky:8080/auth"
REALM = "xencloak"
CLIENT_ID = "xencloak"
CLIENT_SECRET = "79be32ee-9058-4170-8fb4-eefd6e999c4d"  # ou None pour public client

BASE_URI = "http://flasker"
REDIRECT_URI = f"{BASE_URI}/auth/callback"

oauth = OAuth(app)
keycloak = oauth.register(
    name='keycloak',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{KEYCLOAK_SERVER}/realms/{REALM}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'}
)

# --- Configuration de l'API ---
# Remplacez ceci par l'URL de base de votre API si elle est différente
API_BASE_URL = "http://172.17.0.1:5000"

# --- Route de la page d'accueil avec le formulaire ---

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

# --- Route pour l'affichage des réservations ---

def render_reserve(username):
    # Appel à l'API pour obtenir toutes les réservations
    api_url = f"{API_BASE_URL}/api/v1/reservations"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
        datas = response.json()

    except requests.exceptions.RequestException as e:
        # Gérer les erreurs de connexion ou de l'API
        error_message = f"Erreur lors de la communication avec l'API : {e}"
        # On affiche un message d'erreur plus clair dans la page HTML
        return render_template('index.html', 
                               username=username, 
                               reservations=[], 
                               error=error_message)

    # chaque réservation est un dictionnaire avec une clé 'username'
    user_reservations = []

    for res in sorted(datas['reservations'], key=lambda x: x["servername"]):
        if res["username"] == username: user_reservations.append(res)
    
    # Affichage du résultat
    return render_template('index.html', 
                           username=username, 
                           reservations=user_reservations,
                           error=None)

@app.route('/', methods=['GET'])
def show_reservations():
    """
    Récupère le nom d'utilisateur, interroge l'API /api/v1/reservations,
    et filtre les serveurs alloués à cet utilisateur.
    """

    if 'user' not in session:
        return "<a href='/login'>Login with Keycloak</a>"

    # Récupération du nom d'utilisateur depuis le formulaire
    user=session['user']
    username = user['preferred_username']
    
    return(render_reserve(username))

@app.route('/allocations', methods=['POST'])
def allocation():                                                                                                                                                                                    
    """
    Récupère le nom d'utilisateur, interroge l'API /api/v1/reservations,
    et filtre les serveurs alloués à cet utilisateur.
    """

    if 'user' not in session:
        return redirect(url_for('login'))

    # Récupération du nom d'utilisateur depuis le formulaire
    user=session['user']
    username = user['preferred_username']
    cpu = request.form.get('cpu')
    ram = request.form.get('ram')
    
    if not username:
        return "Erreur : Nom d'utilisateur manquant.", 400

    # Appel à l'API pour obtenir toutes les réservations
    api_url = f"{API_BASE_URL}/api/v1/reserve"

    payload = {
        "username": username,
        "cpu": int(cpu),
        "ram": int(ram)
    }

    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(
            api_url,
            headers=headers,
            json=payload # L'argument 'json' gère automatiquement la sérialisation et le header Content-Type
    )
    response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)

    if response.status_code == 200 or response.status_code == 201:
        print("Réservation réussie.")

    return render_reserve(username)

@app.route('/liberation', methods=['GET'])
def liberation():                                                                                                                                                                                    
    """
    Récupère le nom d'utilisateur, interroge l'API /api/v1/reservations,
    et filtre les serveurs alloués à cet utilisateur.
    """

    if 'user' not in session:
        return redirect(url_for('login'))

    # Récupération du nom d'utilisateur depuis le formulaire
    user=session['user']
    username = user['preferred_username']
    servername = request.args.get('servername')
    
    if not username:
        return "Erreur : Nom d'utilisateur manquant.", 400

    # Appel à l'API pour obtenir toutes les réservations
    api_url = f"{API_BASE_URL}/api/v1/release/server/{username}/{servername}"
    print(api_url)
    response = requests.delete(api_url)
    response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)

    if response.status_code == 200 or response.status_code == 201:
        print("Libération réussie.")

    return render_reserve(username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(f"{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/logout?redirect_uri={BASE_URI}")

if __name__ == '__main__':
    # Lancez d'abord votre API principale (si elle n'est pas déjà lancée) !
    # Cette application cliente peut être lancée sur un port différent, par exemple 7777.
    app.run(debug=True, host="0.0.0.0", port=7777)
