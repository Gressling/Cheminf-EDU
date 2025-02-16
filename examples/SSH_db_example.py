import MySQLdb
import sshtunnel

sshtunnel.SSH_TIMEOUT = 10.0
sshtunnel.TUNNEL_TIMEOUT = 10.0

with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com', 22),
    ssh_username='gressling', ssh_password='kinhin100.',
    remote_bind_address=('gressling.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    connection = MySQLdb.connect(
        user='gressling',
        passwd='kinhin100.',
        host='127.0.0.1', port=tunnel.local_bind_port,
        db='gressling$cheminf',
    )
    print(connection)
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM `gressling$cheminf`.`cheminf3_inventory`;")
    cursor.execute("SELECT * FROM gressling$cheminf.cheminf3_molecules;")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    connection.close()