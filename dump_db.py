#!/usr/bin/env python3

from lib import *

resa = xen_reservator()

print("=== SERVERS ===")
for _id, nom, cpu, ram  in resa.get_servers():
    print(f"ID: {_id}, Nom: {nom}, CPU: {cpu}, RAM: {ram}")

print("\n=== USERS ===")
for username in resa.get_users():
    print(username)

print("\n=== RESERVATIONS ===")
for _id, server, user, time in resa.get_reservations():
    print(f"Reservation ID: {_id}, Server: {server}, User: {user}, Time: {time}")

resa.close()
