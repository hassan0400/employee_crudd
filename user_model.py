from flask_login import UserMixin
from config import get_connection

class User(UserMixin):
    def __init__(self, id, username, password, role=None):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return User(row['id'], row['username'], row['password'], row.get('role'))
        return None

    @staticmethod
    def get_user_by_username(username):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return User(row['id'], row['username'], row['password'], row.get('role'))
        return None
