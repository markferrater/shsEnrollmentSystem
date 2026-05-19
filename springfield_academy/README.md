# Springfield Academy — Enrollment Management System

## Project Structure
```
springfield_academy/
├── main.py                  ← Entry point (run this)
├── setup_db.py              ← Run once to create database & tables
├── database_conn.py         ← MySQL connection
├── Logo.png                 ← Place your logo here
├── models/
│   └── login_model.py       ← Authentication logic
├── views/
│   ├── login_window.py      ← Login screen
│   ├── registration_window.py ← Student self-registration
│   ├── student_portal.py    ← Student dashboard, schedule, grades, announcements
│   ├── staff_portal.py      ← Staff: approve/decline students with feedback
│   └── admin_portal.py      ← Admin: dashboard, announcements, accounts, PDF reports
└── styles/
    └── theme.py             ← Color palette & stylesheets
```

## Setup Instructions

### 1. Install dependencies
```bash
pip install PyQt6 pymysql bcrypt matplotlib reportlab
```

### 2. Set up MySQL
Make sure MySQL is running with:
- host: localhost
- user: root
- password: (empty)

Or edit `database_conn.py` with your credentials.

### 3. Create the database
```bash
python setup_db.py
```
This creates all tables and a default admin account:
- **Username:** `admin`
- **Password:** `admin123`

### 4. Copy your Logo
Place `Logo.png` inside the `springfield_academy/` folder.

### 5. Run the app
```bash
python main.py
```

---

## Features

### 🔐 Login
- Role selector: Student / Staff / Admin
- Student accounts show pending/declined messages

### 📝 Student Registration
- 2-step form: Personal info → Enrollment info
- Auto-generates unique LRN
- Bcrypt password hashing
- Submitted as "Pending" for staff review

### 👩‍💼 Staff Portal
- Dashboard with pending/approved/declined counts
- Student Applications table with Approve / Decline buttons
- Feedback message required for both actions
- View all approved students
- View announcements from admin

### 🎓 Student Portal
- Dashboard showing enrollment status + feedback
- Class Schedule (1st & 2nd semester tabs, filtered by strand)
- Grades (1st & 2nd semester, color-coded pass/fail)
- Announcements targeted to students

### ⚙️ Admin Portal
- Dashboard with full stats + pie chart overview
- Post announcements (target: Student / Staff / Both), delete announcements
- View all students with status
- Create Staff and Admin accounts
- **Generate PDF Reports** with:
  - Summary statistics table
  - Enrollment status pie chart
  - Students-by-strand bar chart
  - Full student data table

---

## Notes
- Passwords are hashed with bcrypt
- The `setup_db.py` script is safe to run multiple times (uses IF NOT EXISTS)
- Sample class schedules are auto-inserted for STEM, ABM, and HUMSS
