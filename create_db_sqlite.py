import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
# Le path de la nouvelle db ne peut pas être le même path que le script lui même
if __name__ == '__main__':
    create_connection("/home/hecator/Projet_Python/scrap_data_mx/data_mx.db")