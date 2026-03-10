from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import mysql.connector
from mysql.connector import Error
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ministrypay_secret_2026'

# ── DB CONFIG ──────────────────────────────────────────────
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'ministrypay',
    'user': 'root',
    'password': 'THrenuka*123'          # change to your MySQL password
}

def get_db():
    """Return a new MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None

# ── AUTH DECORATOR ─────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'emp_no' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def welcome():
    return render_template("first.html")

# Route for the SUPER ADMIN main page after successful login
@app.route('/usermain')
def usermain():
    return render_template("usermain.html")

#Route for the user main page after successful login
@app.route("/dashboard")
def nusermain():
    return render_template("dashboard.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
 
        emp_no=request.form['emp_no']
        name=request.form['Name']
        designation=request.form['designation']
        department=request.form['department']
        email=request.form['email']
        password=request.form['password']
        role=request.form['role']

        conn = get_db()

        if conn:
            try:
                cursor = conn.cursor()

                sql = """
                INSERT INTO users 
                (emp_no, name, designation, department, email, password, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                values = (emp_no, name, designation, department, email, password, role)

                cursor.execute(sql, values)

                conn.commit()

                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))

            except Error as e:
                flash(f"Database error: {e}", 'error')
                return redirect(url_for('register'))

            finally:
                cursor.close()
                conn.close()

        else:
            flash('Database connection failed. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

# ── LOGIN ──────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'emp_no' in session:
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        emp_no   = request.form.get('emp_no', '').strip()
        password = request.form.get('password', '').strip()

        conn = get_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE emp_no = %s AND password = %s",
                (emp_no, password)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['emp_no']      = user['emp_no']
                session['name']        = user['name']
                session['designation'] = user['designation']
                session['department']  = user['department']
                session['email']       = user['email']
                session['role']        = user['role']
                
                # Redirect based on role
                if user['role'] == 'admin':
                  return redirect(url_for('usermain'))
                else:
                  return redirect(url_for('dashboard'))
         
                
            else:
                error = 'Invalid Employee Number or Password.'
        else:
            error = 'Database connection failed. Please try again.'

    return render_template('login.html', error=error)

# ── LOGOUT ────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── DASHBOARD (main page) ─────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    emp_no = session['emp_no']
    conn   = get_db()
    latest = None
    recent = []

    if conn:
        cursor = conn.cursor(dictionary=True)

        # Latest salary record
        cursor.execute(
            """SELECT * FROM salary WHERE emp_no = %s
               ORDER BY pay_period DESC LIMIT 1""",
            (emp_no,)
        )
        latest = cursor.fetchone()

        # Last 4 records for overview table
        cursor.execute(
            """SELECT * FROM salary WHERE emp_no = %s
               ORDER BY pay_period DESC LIMIT 4""",
            (emp_no,)
        )
        recent = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('dashboard.html',
                           user=session,
                           latest=latest,
                           recent=recent)

# ── API: LAST 6 MONTHS PAYSLIPS ───────────────────────────
@app.route('/api/payslips')
@login_required
def api_payslips():
    emp_no = session['emp_no']
    conn   = get_db()
    rows   = []

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM salary WHERE emp_no = %s
               ORDER BY pay_period DESC LIMIT 6""",
            (emp_no,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

    # Convert Decimal to float for JSON
    result = []
    for r in rows:
        result.append({
            'id':               r['id'],
            'emp_no':           r['emp_no'],
            'name':             r['name'],
            'designation':      r['designation'],
            'pay_period':       r['pay_period'],
            'status':           r['status'],
                       
            'basic_salary':     float(r['basic_salary']   or 0),
            'language_allowance': float(r['language_allowance'] or 0),
            'coliving':        float(r['coliving'] or 0),
            'telephone_allowance': float(r['telephone_allowance'] or 0),
            'fuel_allowance':   float(r['fuel_allowance'] or 0),
            'executive_allowance': float(r['executive_allowance'] or 0),
            'extra_duty_ot':   float(r['extra_duty_ot'] or 0),
            'basic_arrears':   float(r['basic_arrears'] or 0),
            'total_earnings':   float(r['total_earnings'] or 0),
            
            'wop':             float(r['wop'] or 0),
            'agrahara':        float(r['agrahara'] or 0),
            'apit_tax':        float(r['apit_tax'] or 0),
            'stamp_duty':      float(r['stamp_duty'] or 0),
            'union_fee':       float(r['union_fee'] or 0),
            'news_payment':    float(r['news_payment'] or 0),
            'mileage':         float(r['mileage'] or 0),
            'wop_arrears':     float(r['wop_arrears'] or 0),
            'distress_loan':   float(r['distress_loan'] or 0),
            'total_deductions': float(r['total_deductions'] or 0),
            
            'net_salary':      float(r['net_salary'] or 0),
            
            'remarks':          r['remarks'] or ''
        })

    return jsonify(result)

# ── API: UPDATE PROFILE ───────────────────────────────────
@app.route('/api/update_profile', methods=['POST'])
@login_required
def update_profile():
    data   = request.get_json()
    emp_no = session['emp_no']

    allowed_fields = ['name', 'email']   # only these two are user-editable
    updates = {k: v for k, v in data.items() if k in allowed_fields}

    if not updates:
        return jsonify({'success': False, 'message': 'No valid fields to update.'})

    conn = get_db()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error.'})

    try:
        cursor = conn.cursor()
        set_clause = ', '.join(f"`{k}` = %s" for k in updates)
        values     = list(updates.values()) + [emp_no]
        cursor.execute(
            f"UPDATE users SET {set_clause} WHERE emp_no = %s",
            values
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Refresh session
        for k, v in updates.items():
            session[k] = v

        return jsonify({'success': True, 'message': 'Profile updated successfully.'})
    except Error as e:
        return jsonify({'success': False, 'message': str(e)})

# ── API: CHANGE PASSWORD ──────────────────────────────────
@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    data       = request.get_json()
    emp_no     = session['emp_no']
    current_pw = data.get('current_password', '')
    new_pw     = data.get('new_password', '')

    if not current_pw or not new_pw:
        return jsonify({'success': False, 'message': 'All fields are required.'})

    conn = get_db()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error.'})

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT password FROM users WHERE emp_no = %s", (emp_no,)
    )
    row = cursor.fetchone()

    if not row or row['password'] != current_pw:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Current password is incorrect.'})

    cursor.execute(
        "UPDATE users SET password = %s WHERE emp_no = %s",
        (new_pw, emp_no)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True, 'message': 'Password changed successfully.'})


@app.route('/save_salary', methods=['POST'])
@login_required
def save_salary():

    # Employee details
    emp_no = request.form.get('emp_no',0)
    name = request.form.get('name')
    designation = request.form.get('designation')
    pay_period = request.form.get('pay_period')
    status = request.form.get('status')
    remarks = request.form.get('remarks')

    # Earnings
    basic_salary = float(request.form.get('basic_salary') or 0)
    language_allowance = float(request.form.get('language_allowance') or 0)
    coliving = float(request.form.get('coliving') or 0)
    coliving = float(request.form.get('coliving') or 0)
    telephone_allowance = float(request.form.get('telephone_allowance') or 0)
    fuel_allowance = float(request.form.get('fuel_allowance') or 0)
    executive_allowance = float(request.form.get('executive_allowance') or 0)
    extra_duty_ot = float(request.form.get('extra_duty_ot') or 0)
    basic_arrears = float(request.form.get('basic_arrears') or 0)
    total_earnings = float(request.form.get('total_earnings') or 0)

# Deductions
    wop = float(request.form.get('wop') or 0)
    agrahara = float(request.form.get('agrahara') or 0)
    apit_tax = float(request.form.get('apit_tax') or 0)
    stamp_duty = float(request.form.get('stamp_duty') or 0)
    union_fee = float(request.form.get('union_fee') or 0)
    news_payment = float(request.form.get('news_payment') or 0)
    mileage = float(request.form.get('mileage') or 0)
    wop_arrears = float(request.form.get('wop_arrears') or 0)
    distress_loan = float(request.form.get('distress_loan') or 0)
    total_deductions = float(request.form.get('total_deductions') or 0)

# Net Salary
    net_salary = float(request.form.get('net_salary') or 0)



    conn = get_db()

    if not conn:
        return jsonify({'success': False, 'message': 'Database error'})

    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO salary (
            emp_no, name, designation,
            basic_salary, language_allowance, coliving,
            telephone_allowance, fuel_allowance, executive_allowance,
            extra_duty_ot, basic_arrears, total_earnings,
            wop, agrahara, apit_tax, stamp_duty, union_fee,
            news_payment, mileage, wop_arrears, distress_loan,
            total_deductions,net_salary, pay_period, status, remarks
        )
        VALUES (
            %s,%s,%s,
            %s,%s,%s,
            %s,%s,%s,
            %s,%s,%s,
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,
            %s,%s,%s,%s,%s
        )
        """

        values = (
            emp_no, name, designation,
            basic_salary, language_allowance, coliving,
            telephone_allowance, fuel_allowance, executive_allowance,
            extra_duty_ot, basic_arrears, total_earnings,
            wop, agrahara, apit_tax, stamp_duty, union_fee,
            news_payment, mileage, wop_arrears, distress_loan,
            total_deductions,net_salary, pay_period, status, remarks
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()
        flash('Salary record saved successfully.', 'success')
        return redirect(url_for('usermain'))
        

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})



# ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
