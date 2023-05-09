import sqlite3


class DataBase:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id TEXT,
         active TEXT, long TEXT)''')

    def user_exists(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(result))


    def create_user(self, user_id):
        with self.conn:
            self.cursor.execute(f"INSERT INTO users (user_id, active) VALUES ('{user_id}', '1')")
            self.conn.commit()

    def get_users(self):
        with self.conn:
            self.cursor.execute("SELECT * FROM users")
            rows = self.cursor.fetchall()
            return rows
