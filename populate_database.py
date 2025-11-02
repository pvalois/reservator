#!/usr/bin/env python3
import pymysql
import configparser

# --- Lire la config ---
config = configparser.ConfigParser()
config.read('mariadb.ini')

host = config.get('mysql', 'host')
port = config.getint('mysql', 'port', fallback=3306)
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')

# --- Connexion à xen_pxe_oc ---
conn = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database="xen_pxe_oc",
    autocommit=True
)
cur = conn.cursor()

# --- 10 serveurs ---
servers = [
    ("serv001", 32, 32),
    ("serv002", 16, 128),
    ("serv003", 16, 128),
    ("serv004", 16, 64),
    ("serv005", 64, 128),
    ("serv006", 16, 128),
    ("serv007", 64, 64),
    ("serv008", 64, 32),
    ("serv009", 16, 128),
    ("serv010", 16, 32)
]

for nom, cpu, ram in servers:
    cur.execute("INSERT IGNORE INTO servers (nom, cpu, ram) VALUES (%s, %s, %s);", (nom, cpu, ram))

print("✅ Users et servers insérés avec succès ! Aucune réservation initiale.")

cur.close()
conn.close()

