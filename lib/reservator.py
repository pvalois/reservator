import pymysql
import configparser

class xen_reservator:

    conn=None
    cursor=None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('mariadb.ini')

        host = config.get('mysql', 'host')
        port = config.getint('mysql', 'port', fallback=3306)
        user = config.get('mysql', 'user')
        password = config.get('mysql', 'password')

        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database="xen_pxe_oc",
            autocommit=True
        )

        self.conn = conn
        self.cursor = conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_servers(self):
        self.cursor.execute("SELECT id, nom, cpu, ram FROM servers ORDER BY id;")
        servers = self.cursor.fetchall()
        for s in servers:
            yield(s[0],s[1], s[2], s[3])

    def get_users(self):
        self.cursor.execute("SELECT uid FROM users ORDER BY uid;")
        users = self.cursor.fetchall()
        for u in users:
            yield(u[0])

    def get_reservations(self):
        query="""
              SELECT r.id, s.nom, u.uid, r.reservation_time
              FROM reservations r
              JOIN servers s ON r.idserveur = s.id
              JOIN users u ON r.iduser = u.uid
              ORDER BY r.id;
              """
        self.cursor.execute(query)
        reservations = self.cursor.fetchall()
        for r in reservations:
          yield(r[0],r[1],r[2],r[3])

    def get_free_server(self, username:str, cpu:int, ram:int):
        """ Nous utilisons une fonction de calcul de perte pondérée : L_rel_n = ((Cn - X) / Cn) + alpha * ((Rn - Y) / Rn)
            afin de donner plus d'impotance à la perte de ram qu'a la perte de cpu lors des affectations,
            sur la base que chaque process peut demander autant de ram qu'il veut sans consommer de cpu.
            Nos utilisateurs voulant une ram précise, on se fiche que le cpu dorme ..."""

        query="""
              SELECT s.id, s.nom, s.cpu, s.ram,
                   -- Calcul de la Perte Relative Pondérée (L_rel_n)
                   (((s.cpu - %s) * 1.0 / s.cpu) + ( %s * ( (s.ram - %s) * 1.0 / s.ram ))) AS weighted_loss
              FROM servers s
            
              -- Utiliser LEFT JOIN pour ramener les lignes de 'servers' même sans correspondance
              LEFT JOIN reservations r ON s.id = r.idserveur
            
              -- 1. Contrainte d'Exclusivité (Serveur non alloué/réservé)
              WHERE r.idserveur IS NULL 
            
              -- 2. Contraintes d'Éligibilité (Capacités suffisantes)
              AND s.cpu >= %s AND s.ram >= %s
            
              -- 3. Minimisation de la perte
              ORDER BY weighted_loss ASC 
            
              LIMIT 1
              FOR UPDATE;
              """

        self.conn.begin()
        self.cursor.execute(query,(cpu, 2.0, ram, cpu, ram))
        server_found = self.cursor.fetchone()

        if not server_found:
            self.conn.rollback()
            return(None)

        server_id, servername, server_cpu, server_ram, loss = server_found
        self.cursor.execute("INSERT INTO reservations (idserveur, iduser) VALUES (%s, %s)", (server_id, username))
        self.conn.commit()

        return(server_id, servername, server_cpu, server_ram)

    def release_by_id(self, _id:int):
        query="""
              DELETE 
              FROM reservations
              WHERE id = %s
              """

        self.cursor.execute(query,(_id))
        return(self.cursor.rowcount)

    def release_server(self, username:str, servername:str):
        query="""
              DELETE r
              FROM reservations r
              JOIN servers s ON r.idserveur = s.id
              WHERE s.nom = %s AND r.iduser = %s
              """

        self.cursor.execute(query,(servername, username))
        return(self.cursor.rowcount)



