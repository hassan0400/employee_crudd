from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required
from models.employee_model import Employee

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/dashboard')
@login_required
def dashboard():
    employees = Employee.get_all()
    return render_template('dashboard.html', employees=employees)

@employee_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        emp = Employee(
            name=request.form['name'],
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password'],
            city=request.form['city'],
            photo=request.files['photo']
        )
        emp.save(upload_folder=current_app.config['UPLOAD_FOLDER'])
        flash("Employee added successfully!")
        return redirect(url_for('employee.dashboard'))

    return render_template('add.html')

# Optional: AJAX list endpoint
@employee_bp.route('/api/list')
@login_required
def api_list():
    employees = Employee.get_all()
    return jsonify([
        {
            'id': emp[0],
            'name': emp[1],
            'username': emp[2],
            'email': emp[3],
            'city': emp[5],
            'photo': emp[6]
        } for emp in employees
    ])
