#!/usr/bin/env python3

from lib import *
from flask import Flask, request, jsonify, abort
from typing import Dict, Any, List

app = Flask(__name__)

# Créer une instance globale de votre classe Reservator
reservator = xen_reservator()

# --- Routes (Endpoints) de l'API ---

## Routes d'information (GET)

@app.route('/api/v1/servers', methods=['GET'])
def servers_list():
    """Récupère la liste de tous les serveurs et leurs capacités."""

    raw = reservator.get_servers()
    formatted = []
    for res in raw:
        _id, servername, cpu, ram= res
        _dict = {
            "id": _id,
            "servername": servername,
            "cpu": cpu,
            "ram": ram 
            # Ajoutez toutes les autres informations que vous souhaitez exposer
        }
        formatted.append(_dict)

    response_data = {
        "status": "success",
        "count": len(formatted),
        "reservations": formatted
    }

    return jsonify(response_data)

@app.route('/api/v1/reservations', methods=['GET'])
def reservations_list():
    """Récupère la liste des réservations en cours."""
    raw= reservator.get_reservations()
    formatted= []
    for res in raw:
        reservation_id, servername, username, date = res
        _dict = {
            "reservation_id": reservation_id,
            "servername": servername,
            "username": username,
            "date": date
            # Ajoutez toutes les autres informations que vous souhaitez exposer
        }
        formatted.append(_dict)

    response_data = {
        "status": "success",
        "count": len(formatted),
        "reservations": formatted
    }

    return jsonify(response_data)

## Route d'Allocation (POST)

@app.route('/api/v1/reserve', methods=['POST'])
def allocate_server():
    """
    Tente de trouver et d'allouer un serveur optimal selon les critères.
    Body JSON attendu : {"username": "user_name", "cpu": 18, "ram": 50}
    """
    data = request.get_json()
    
    # Validation des données
    username = data.get('username')
    cpu = data.get('cpu')
    ram = data.get('ram')
    
    if not all([username, isinstance(cpu, int), isinstance(ram, int)]):
        return jsonify({"status": "error", "message": "Les champs username, cpu (int) et ram (int) sont requis."}), 400

    server = reservator.get_free_server(username, cpu, ram)
    
    if server:
        # Le serveur a été trouvé et la réservation a été enregistrée en BDD
        return jsonify({
            "status": "success",
            "message": f"Serveur {server[1]} alloué avec succès.",
            "server": server[1]
        }), 201
    else:
        return jsonify({
            "status": "fail",
            "message": "Aucun serveur éligible trouvé ou les ressources sont insuffisantes."
        }), 200

@app.route('/api/v1/release/id/<int:reservation_id>', methods=['DELETE'])
def release_by_reservation_id(reservation_id: int):
    """Libère une réservation en utilisant son ID."""
    if reservator.release_by_id(reservation_id):
        return jsonify({"status": "success", "message": f"Réservation ID {reservation_id} libérée."})
    else:
        return jsonify({"status": "fail", "message": f"Réservation ID {reservation_id} non trouvée ou échec de libération."}), 200

@app.route('/api/v1/release/server/<string:username>/<string:servername>', methods=['DELETE'])
def release_by_user_and_server(username: str, servername: str):
    """Libère une réservation en utilisant le nom d'utilisateur et le nom du serveur."""
    if reservator.release_server(username, servername):
        return jsonify({"status": "success", "message": f"Serveur '{servername}' libéré pour l'utilisateur '{username}'."})
    else:
        return jsonify({"status": "fail", "message": f"Aucune réservation correspondante trouvée pour {username} sur {servername}."}), 200

if __name__ == '__main__':
    # Utilisez 'debug=True' pour le développement (à désactiver en production)
    app.run(debug=True, host="0.0.0.0", port=5000)
    reservator.close()
