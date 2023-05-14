import psycopg2


class DataBase:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

        self.conn = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, user_id TEXT,
         active TEXT, long TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (id SERIAL PRIMARY KEY, token TEXT,
         active TEXT)''')

    def user_exists(self, user_id):
        with self.conn:
            self.cursor.execute("SELECT * FROM users WHERE user_id = %s::text", (user_id,))
            result = self.cursor.fetchall()
            return len(result) > 0
            


    def create_user(self, user_id):
        with self.conn:
            self.cursor.execute("INSERT INTO users (user_id, active) VALUES (%s, '1')", (user_id,))
            self.conn.commit()

    def create_token(self, token):
        with self.conn:
            self.cursor.execute("INSERT INTO tokens (token, active) VALUES (%s, '1')", (token,))
            self.conn.commit()

    def get_tokens(self):
        with self.conn:
            self.cursor.execute("SELECT * FROM tokens")
            rows = self.cursor.fetchall()
            return rows
    
    def delete_token(self, token):
        with self.conn:
            self.cursor.execute("DELETE FROM tokens WHERE token = %s", (token,))
            self.conn.commit()

    def get_users(self):
        with self.conn:
            self.cursor.execute("SELECT * FROM users")
            rows = self.cursor.fetchall()
            return rows

    def get_users_active(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT active FROM users WHERE user_id = %s", (user_id,))
            return result[0][0]

if __name__ == "__main__":
    print()     
