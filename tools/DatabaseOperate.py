import sqlite3


class DataBase:
    def __init__(self, webpage_name: str):
        self.db_name = 'Databases/html_codes.db'
        self.tb_name = webpage_name

    def record_file(self, html_code1: bytes):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.tb_name}")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.tb_name} (id INTEGER PRIMARY KEY, html_code BLOB)")

        cursor.execute(f"INSERT INTO {self.tb_name} (html_code) VALUES (?)", (html_code1,))
        conn.commit()
        conn.close()

    def read_file(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {self.tb_name}")

        # Fetch all the rows returned by the SELECT statement
        rows = cursor.fetchall()
        conn.close()
        return rows[0][1]
