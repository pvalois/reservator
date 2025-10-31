#!/usr/bin/env python3

import json
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# --- Configuration de l'API ---
# Remplacez ceci par l'URL de base de votre API si elle est différente
API_BASE_URL = "http://127.0.0.1:5000"

# --- Route de la page d'accueil avec le formulaire ---

@app.route('/', methods=['GET'])
def index():
    """Affiche le formulaire de saisie du nom d'utilisateur."""
    # Le template 'index.html' sera responsable de l'affichage du formulaire.
    return render_template('index.html')

# --- Route pour l'affichage des réservations ---

@app.route('/reservations', methods=['POST'])
def show_reservations():
    """
    Récupère le nom d'utilisateur, interroge l'API /api/v1/reservations,
    et filtre les serveurs alloués à cet utilisateur.
    """

    # Récupération du nom d'utilisateur depuis le formulaire
    username = request.form.get('username')
    
    if not username:
        return "Erreur : Nom d'utilisateur manquant.", 400

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
        return render_template('reservations.html', 
                               username=username, 
                               reservations=[], 
                               error=error_message)

    print (datas['reservations'])

    # chaque réservation est un dictionnaire avec une clé 'username'
    user_reservations = []

    for res in datas['reservations']:
        if res["username"] == username: user_reservations.append(res)

    
    # Affichage du résultat
    return render_template('reservations.html', 
                           username=username, 
                           reservations=user_reservations,
                           error=None)

@app.route('/allocations', methods=['POST'])
def allocation():                                                                                                                                                                                    
    """
    Récupère le nom d'utilisateur, interroge l'API /api/v1/reservations,
    et filtre les serveurs alloués à cet utilisateur.
    """

    # Récupération du nom d'utilisateur depuis le formulaire
    username = request.form.get('username')
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
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload # L'argument 'json' gère automatiquement la sérialisation et le header Content-Type
        )
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
        if response.status_code == 200 or response.status_code == 201:
            print("Réservation réussie.")

    except requests.exceptions.RequestException as e:
        # Gérer les erreurs de connexion ou de l'API
        error_message = f"Erreur lors de la communication avec l'API : {e}"
        # On affiche un message d'erreur plus clair dans la page HTML
        return render_template('reservations.html', 
                               username=username, 
                               reservations=[], 
                               error=error_message)

        
        datas = response.json()
        print (datas)

    # Affichage du résultat
    return render_template('allocations.html', 
                           username=username, 
                           reservations=[],
                           error=None)

if __name__ == '__main__':
    # Lancez d'abord votre API principale (si elle n'est pas déjà lancée) !
    # Cette application cliente peut être lancée sur un port différent, par exemple 5001.
    app.run(debug=True, port=5001)
