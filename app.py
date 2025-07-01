from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import pymysql
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Upload folder path
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL connection
# MySQL connection
try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_db",
        port=3306
    )
    cursor = conn.cursor()

    # ✅ Fix for table structure cache issues
    cursor.execute("SET SQL_QUOTE_SHOW_CREATE=1")

except pymysql.MySQLError as e:
    print("Error connecting to MySQL:", e)
    exit()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(id=user[0], username=user[1])
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT id, username FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            login_user(User(id=user[0], username=user[1]))
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        photo = request.files['photo']
        photo_name = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_name)
        photo.save(photo_path)

        sql = "INSERT INTO employees (name, username, email, password, city, photo) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, username, email, password, city, photo_name)
        cursor.execute(sql, val)
        conn.commit()

        flash('Employee added successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('dashboard.html', employees=employees)

# ✅ Attendance Dashboard Route
@app.route('/attendance_dashboard')
@login_required
def attendance_dashboard():
    today = datetime.today().date()

    # Get total present today
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE DATE(date)=%s AND sign_in IS NOT NULL", (today,))
    total_present = cursor.fetchone()[0]

    # Total employees
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    total_absent = total_employees - total_present

    # Get full attendance records
    cursor.execute("""
        SELECT e.name, a.date, a.sign_in, a.sign_out
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        ORDER BY a.date DESC
    """)
    records = cursor.fetchall()

    return render_template('attendance_dashboard.html',
                           records=records,
                           total_present=total_present,
                           total_absent=total_absent)

# ✅ QR Code Scanner Page
@app.route('/qrcode')
@login_required
def qrcode():
    return render_template('qrcode.html')

# ✅ Fix for missing scan endpoint (used in url_for('scan'))
@app.route('/scan')
@login_required
def scan():
    return render_template('qrcode.html')  # You can use same or separate template

# ✅ Run App
if __name__ == '__main__':
    app.run(debug=True)
