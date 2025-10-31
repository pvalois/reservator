#!/usr/bin/env python3

import argparse
from lib import *

# --- Argparse ---
parser = argparse.ArgumentParser(description="Libérer une réservation de serveur")
parser.add_argument('-i', '--id', type=str, help='Nom du serveur à libérer')
parser.add_argument('-s', '--serveur', type=str, help='Nom du serveur à libérer')
parser.add_argument('-u', '--utilisateur', type=str, help='Nom de l\'utilisateur')
args = parser.parse_args()

resa = xen_reservator()

if (args.serveur):
  serveur_nom = args.serveur
  utilisateur = args.utilisateur
  count=resa.release_server(utilisateur, serveur_nom)

if (args.id):
  count=resa.release_by_id(args.id)

resa.close()

print (f'{count} reservations supprimées')

