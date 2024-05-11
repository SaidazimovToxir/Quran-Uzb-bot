import sqlite3
import threading

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('quran_bot_users.db')
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        create_table = """
            CREATE TABLE IF NOT EXISTS quran_bot_users(
                NAME TEXT,
                USERNAME TEXT,
                USER_ID TEXT UNIQUE,
                CREATED_DT DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.cursor.execute(create_table)
        self.conn.commit()

    def add_users(self, name: str, username: str, user_id: str):
        conn = sqlite3.connect('quran_bot_users.db')
        cursor = conn.cursor()

        select_query = 'SELECT USER_ID FROM quran_bot_users WHERE USER_ID = ?;'
        cursor.execute(select_query, (user_id,))
        data = cursor.fetchone()

        if data is None:
            add_users = "INSERT INTO quran_bot_users(NAME, USERNAME, USER_ID) VALUES (?, ?, ?);"
            values = (name, username, user_id)
            cursor.execute(add_users, values)
            conn.commit()
            conn.close()
            return "Foydalanuvchi yaratildi"
        conn.close()
        return "Foydalanuvchi mavjud"

    def users_info(self):
        conn = sqlite3.connect('quran_bot_users.db')
        cursor = conn.cursor()

        select_query = 'SELECT * FROM quran_bot_users;'
        cursor.execute(select_query)
        data = cursor.fetchall()
        conn.close()
        return data

    def __del__(self):
        self.conn.close()


# Usage example:
db = Database()
# print(db.add_users("jalolov.de ☘️", "jalolv_de", "5300379153"))
# print(db.users_info())