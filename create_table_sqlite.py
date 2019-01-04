import sqlite3
from sqlite3 import Error

# On créé une connection à la base de données
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
# Fonction pour créer la table
def create_table(conn, statement):
    try:
        c = conn.cursor()
        c.execute(statement)
    except Error as e:
        print(e)

def main():
    database = "/home/hecator/Projet_Python/scrap_data_mx/database/data_mx.db"
 
    sql_create_table_mx = """ CREATE TABLE IF NOT EXISTS data_mx_code_iso_country (
                                        id INTEGER PRIMARY KEY,
                                        country_name TEXT NOT NULL,
                                        ISO_3166_1_alpha TEXT NOT NULL, 
                                        IOS_3166_1_int TEXT NOT NULL
                                    ); """
 
    # On crée la connexion à la base de données
    conn = create_connection(database)
    if conn is not None:
        # On créé la table en fonction du statement
        create_table(conn, sql_create_table_mx)

    else:
        print("Erreur! Connection à la DB impossible.")

# On lance le tout
if __name__ == '__main__':
    main()