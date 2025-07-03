from config import get_connection
from werkzeug.utils import secure_filename
import os

class Employee:
    def __init__(self, name, username, email, password, city, photo):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.city = city
        self.photo = photo

    def save(self, upload_folder):
        conn = get_connection()
        cursor = conn.cursor()

        photo_name = secure_filename(self.photo.filename)
        photo_path = os.path.join(upload_folder, photo_name)
        self.photo.save(photo_path)

        sql = "INSERT INTO employees (name, username, email, password, city, photo) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (self.name, self.username, self.email, self.password, self.city, photo_name)
        cursor.execute(sql, val)
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees")
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result
