from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user_model import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.authenticate(request.form['username'], request.form['password'])
        if user:
            login_user(user)
            flash("Login successful!")
            return redirect(url_for('employee.dashboard'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out!")
    return redirect(url_for('auth.login'))
