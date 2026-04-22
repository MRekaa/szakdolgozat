import json

try:
    import mysql.connector
except ImportError:
    mysql = None

class DatabaseManager:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '', 
            'host': 'localhost',
            'database': 'labor'
        }

    def _connect(self):
        if mysql is None:
            raise RuntimeError('mysql.connector modul nincs telepítve')
        return mysql.connector.connect(**self.config)

    def get_all_reactions(self):
        return self._fetch_rows('reactions')

    def get_all_materials(self):
        return self._fetch_names('materials')

    def get_all_tools(self):
        return self._fetch_names('tools')

    def _fetch_rows(self, table_name):
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as err:
            print(f"Adatbázis hiba ({table_name}): {err}")
            return []

    def _fetch_names(self, table_name):
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT name FROM {table_name}")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [row['name'] for row in rows if 'name' in row]
        except Exception as err:
            print(f"Adatbázis hiba ({table_name}): {err}")
            return []