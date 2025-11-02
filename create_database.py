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
cur.execute("CREATE DATABASE IF NOT EXISTS xen_pxe_oc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
print("✅ Base xen_pxe_oc créée (si elle n'existait pas).")

# --- Donner tous les droits à admin ---
cur.execute(f"GRANT ALL PRIVILEGES ON xen_pxe_oc.* TO '{admin_user}'@'%'")
cur.execute("FLUSH PRIVILEGES;")
print(f"✅ Tous les droits sur xen_pxe_oc attribués à {admin_user}.")

# --- Se connecter maintenant directement sur xen_pxe_oc avec admin ---
conn.close()

conn = pymysql.connect(
    host=host,
    port=port,
    user=admin_user,
    password=config.get('mysql', 'password'),
    database="xen_pxe_oc",
    autocommit=True
)
cur = conn.cursor()

# --- Créer les tables ---

# Table servers
cur.execute("""
CREATE TABLE IF NOT EXISTS servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    cpu INT NOT NULL,
    ram INT NOT NULL
) ENGINE=InnoDB;
""")

# Table reservations
cur.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idserveur INT NOT NULL,
    iduser VARCHAR(100) NOT NULL,
    reservation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idserveur) REFERENCES servers(id) ON DELETE CASCADE,
    UNIQUE KEY unique_reservation (idserveur)
) ENGINE=InnoDB;
""")

print("Nombre de lignes affectées :", cur.rowcount)

print("✅ Tables servers, et reservations créées avec succès !")

cur.close()
conn.close()
