from flask import Blueprint, render_template
from flask_login import login_required

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/dashboard')
@login_required
def attendance_dashboard():
    return render_template('attendance_dashboard.html')
