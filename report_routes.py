from flask import Blueprint, render_template, send_file, request
from config import cursor
from openpyxl import Workbook
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

report_bp = Blueprint('report', __name__)

@report_bp.route('/employee')
def employee_report():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('reports/employee_report.html', employees=employees)

@report_bp.route('/attendance')
def attendance_report():
    date = request.args.get('date')
    if date:
        cursor.execute("""
            SELECT e.name, a.date, a.sign_in, a.sign_out
            FROM attendance a
            JOIN employees e ON a.employee_id = e.id
            WHERE DATE(a.date) = %s
        """, (date,))
    else:
        cursor.execute("""
            SELECT e.name, a.date, a.sign_in, a.sign_out
            FROM attendance a
            JOIN employees e ON a.employee_id = e.id
        """)
    records = cursor.fetchall()
    return render_template('reports/attendance_report.html', records=records, date=date)

# XLSX Export
@report_bp.route('/export/employees/xlsx')
def export_employees_xlsx():
    cursor.execute("SELECT name, username, email, city FROM employees")
    data = cursor.fetchall()

    wb = Workbook()
    ws = wb.active
    ws.append(['Name', 'Username', 'Email', 'City'])
    for row in data:
        ws.append(row)

    file = BytesIO()
    wb.save(file)
    file.seek(0)
    return send_file(file, download_name='employees.xlsx', as_attachment=True)

# PDF Export
@report_bp.route('/export/employees/pdf')
def export_employees_pdf():
    cursor.execute("SELECT name, username, email, city FROM employees")
    employees = cursor.fetchall()
    html = render_template('reports/employee_report.html', employees=employees, export=True)

    pdf_file = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=pdf_file)
    pdf_file.seek(0)
    return send_file(pdf_file, download_name="employees.pdf", as_attachment=True)
