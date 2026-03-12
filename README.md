# 🏥 Ministry of Health Sri Lanka — Salary Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)

A secure, web-based salary management portal for Ministry of Health employees.  
Supports payroll entry, payslip viewing, employee management, and role-based access control.

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
  - [Step 1 — Install Python](#step-1--install-python)
  - [Step 2 — Clone the Repository](#step-2--clone-the-repository)
  - [Step 3 — Create Virtual Environment](#step-3--create-virtual-environment)
  - [Step 4 — Install Dependencies](#step-4--install-dependencies)
  - [Step 5 — Set Up MySQL Database](#step-5--set-up-mysql-database)
  - [Step 6 — Configure the Application](#step-6--configure-the-application)
  - [Step 7 — Run the Application](#step-7--run-the-application)
- [Default Login](#-default-login)
- [Usage Guide](#-usage-guide)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Role-Based Login | Separate dashboards for **Admin** and **Employee** roles |
| 📝 Salary Entry | Enter full payroll with earnings, deductions, and auto-calculated net salary |
| 📋 Salary Records | View, search, filter, update, and delete salary records |
| 👁 Payslip View | Detailed payslip modal per employee per period |
| 👥 Employee Directory | Browse all registered employees |
| 🔒 Secure Registration | Password validation + duplicate account detection |
| 📱 Responsive UI | Works on desktop and tablet browsers |

---

## 💻 System Requirements

Before you begin, make sure your machine has the following installed:

| Software | Minimum Version | Download |
|---|---|---|
| Python | 3.8+ | https://www.python.org/downloads/ |
| pip | 21+ | Included with Python |
| MySQL Server | 8.0+ | https://dev.mysql.com/downloads/ |
| Git | Any | https://git-scm.com/downloads |
| Web Browser | Chrome / Firefox / Edge | — |

---

## 📁 Project Structure

```
ministry-salary/
│
├── app.py                  # Main Flask application & all routes
│
├── templates/              # HTML templates (Jinja2)
│   ├── first.html          # Welcome / landing page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── usermain.html       # Admin dashboard
│   └── dashboard.html      # Employee dashboard
│
├── static/                 # Static assets (if any)
│   ├── css/
│   └── js/
│
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🚀 Installation Guide

Follow these steps carefully to get the system running on your local machine.

---

### Step 1 — Install Python

1. Go to https://www.python.org/downloads/
2. Download **Python 3.8 or higher**
3. Run the installer
   - ✅ Make sure to check **"Add Python to PATH"** during installation
4. Verify installation by opening a terminal and running:

```bash
python --version
```

You should see something like: `Python 3.11.4`

---

### Step 2 — Clone the Repository

Open a terminal (Command Prompt / PowerShell / Terminal) and run:

```bash
git clone https://github.com/YOUR_USERNAME/ministry-salary.git
```

Then navigate into the project folder:

```bash
cd ministry-salary
```

> 💡 If you don't have Git, you can also download the ZIP from GitHub and extract it.

---

### Step 3 — Create Virtual Environment

It is recommended to use a virtual environment to keep dependencies isolated.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal prompt.

---

### Step 4 — Install Dependencies

With the virtual environment active, install all required packages:

```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt` yet, install manually:

```bash
pip install flask mysql-connector-python
```

Then generate the requirements file for future use:

```bash
pip freeze > requirements.txt
```

---

### Step 5 — Set Up MySQL Database

#### 5.1 — Start MySQL Server

Make sure your MySQL Server is running. You can use:
- **MySQL Workbench** (GUI)
- **XAMPP / WAMP** (includes MySQL)
- Or the MySQL command line

#### 5.2 — Create the Database

Open MySQL Workbench or the MySQL terminal and run:

```sql
CREATE DATABASE ministrypay;
USE ministrypay;
```

#### 5.3 — Create the `users` Table

```sql
CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    emp_no      VARCHAR(20)  NOT NULL UNIQUE,
    name        VARCHAR(100) NOT NULL,
    designation VARCHAR(100),
    department  VARCHAR(100),
    email       VARCHAR(150) UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('admin', 'employee') DEFAULT 'employee',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.4 — Create the `salary` Table

```sql
CREATE TABLE salary (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    emp_no               VARCHAR(20),
    name                 VARCHAR(100),
    designation          VARCHAR(100),

    -- Earnings
    basic_salary         DECIMAL(12,2) DEFAULT 0,
    language_allowance   DECIMAL(12,2) DEFAULT 0,
    coliving             DECIMAL(12,2) DEFAULT 0,
    telephone_allowance  DECIMAL(12,2) DEFAULT 0,
    fuel_allowance       DECIMAL(12,2) DEFAULT 0,
    executive_allowance  DECIMAL(12,2) DEFAULT 0,
    extra_duty_ot        DECIMAL(12,2) DEFAULT 0,
    basic_arrears        DECIMAL(12,2) DEFAULT 0,
    total_earnings       DECIMAL(12,2) DEFAULT 0,

    -- Deductions
    wop                  DECIMAL(12,2) DEFAULT 0,
    agrahara             DECIMAL(12,2) DEFAULT 0,
    apit_tax             DECIMAL(12,2) DEFAULT 0,
    stamp_duty           DECIMAL(12,2) DEFAULT 0,
    union_fee            DECIMAL(12,2) DEFAULT 0,
    news_payment         DECIMAL(12,2) DEFAULT 0,
    mileage              DECIMAL(12,2) DEFAULT 0,
    wop_arrears          DECIMAL(12,2) DEFAULT 0,
    distress_loan        DECIMAL(12,2) DEFAULT 0,
    total_deductions     DECIMAL(12,2) DEFAULT 0,

    -- Net
    net_salary           DECIMAL(12,2) DEFAULT 0,

    -- Meta
    pay_period           VARCHAR(10),
    status               ENUM('paid','pending') DEFAULT 'pending',
    remarks              TEXT,
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.5 — Create a Default Admin Account

```sql
INSERT INTO users (emp_no, name, designation, department, email, password, role)
VALUES ('ADMIN001', 'Admin User', 'Super Admin', 'Administration', 'admin@health.gov.lk', 'Admin@123', 'admin');
```

> ⚠️ Change this password after first login.

---

### Step 6 — Configure the Application

Open `app.py` and update the database configuration section with your MySQL credentials:

```python
DB_CONFIG = {
    'host':     '127.0.0.1',
    'database': 'ministrypay',
    'user':     'root',           # your MySQL username
    'password': '***********'   # your MySQL password
}
```

Also update the secret key to something secure:

```python
app.secret_key = 'change_this_to_a_strong_random_key'
```

---

### Step 7 — Run the Application

With the virtual environment active, start the Flask server:

```bash
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

🎉 The system is now running!

---

## 🔑 Default Login

| Field | Value |
|---|---|
| Employee No | `ADMIN001` |
| Password | `Admin@123` |
| Role | Super Admin |

> Change the password immediately after first login.

---

## 📖 Usage Guide

### Admin (Super Admin)
- Log in with an `admin` role account
- Use **Enter Salary** to add payroll records for any employee
- Use **View Salary Details** to search, filter, view, edit, or delete records
- Use **All Employees** to browse the employee directory

### Employee
- Log in with your Employee Number and password
- View your own salary history and payslips
- Update your profile and change your password

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: flask` | Run `pip install flask` with your virtual environment active |
| `mysql.connector.errors.DatabaseError` | Check your `DB_CONFIG` credentials in `app.py` |
| `Access denied for user 'root'` | Verify your MySQL username and password |
| Page shows `Internal Server Error` | Run with `debug=True` and check the terminal for the full error |
| Port 5000 already in use | Change the port: `app.run(port=5001)` |
| Templates not found | Make sure all HTML files are inside the `templates/` folder |

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is developed for internal use by the **Ministry of Health, Democratic Socialist Republic of Sri Lanka**.

---

<div align="center">
  Ministry of Health · Democratic Socialist Republic of Sri Lanka<br>
  Salary Management System v2.0
</div>
