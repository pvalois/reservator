#!/usr/bin/env python3

import argparse
from lib import *

# --- Argparse ---
parser = argparse.ArgumentParser(description="Réserver un serveur")
parser.add_argument('-u', '--utilisateur', type=str, required=True, help='Nom de l\'utilisateur')
parser.add_argument('-c', '--cpu', type=int, default=1, help='CPU requis')
parser.add_argument('-m', '--memory', type=int, default=1, help='RAM requise (Go)')
args = parser.parse_args()

utilisateur = args.utilisateur
req_cpu = args.cpu
req_ram = args.memory

resa = xen_reservator()
serveur = resa.get_free_server(utilisateur,req_cpu,req_ram)

if serveur:
    serveur_id, serveur_nom, serveur_cpu, serveur_ram = serveur
    print(f"Serveur pré-affecté pour {utilisateur} : {serveur_nom} (CPU: {serveur_cpu}, RAM: {serveur_ram})")
else:
    print(f"Impossible d'effectuer cette demande")

resa.close()
