import sqlite3
import pandas as pd


class DataBase:
    def __init__(self, webpage_name: str):
        self.db_name = 'Databases/texts_for_analysis.db'
        self.tb_name = webpage_name

        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.tb_name} (id INTEGER PRIMARY KEY, title TEXT, "
                            f"flair TEXT, content TEXT)")

    def insert_record(self, title, flair, content):

        self.cursor.execute(f"INSERT INTO {self.tb_name} (title, flair, content) VALUES (?, ?, ?)",
                            (title, flair, content))
        self.conn.commit()

    def return_records_df(self):
        query = f"SELECT title, flair, content FROM {self.tb_name}"
        return pd.read_sql_query(query, self.conn)

    def close(self):
        self.cursor.close()
        self.conn.close()
