#!/usr/bin/env python3
import pymysql
import configparser

# --- Lire la config ---
config = configparser.ConfigParser()
config.read('mariadb.ini')

host = config.get('mysql', 'host')
port = config.getint('mysql', 'port', fallback=3306)
root_user = config.get('mysql', 'root_user', fallback='root')
root_password = config.get('mysql', 'root_password')

admin_user = config.get('mysql', 'user', fallback='admin')

# --- Connexion MariaDB en root ---
conn = pymysql.connect(
    host=host,
    port=port,
    user=root_user,
    password=root_password,
    autocommit=True
)
cur = conn.cursor()

# --- Créer la base si elle n'existe pas ---
cur.execute("DROP DATABASE xen_pxe_oc")
print("✅ Base xen_pxe_oc détruite")
