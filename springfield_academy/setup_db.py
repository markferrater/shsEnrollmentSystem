"""
Run this ONCE to set up the enrollment_database tables.
Usage: python setup_db.py
"""
import pymysql
import bcrypt

connection = pymysql.connect(
    host='localhost',
    user='root',
    password=''
)
cursor = connection.cursor()

DB = 'enrollment_database'
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB}")
cursor.execute(f"USE {DB}")

# ── student_info ──────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lrn_id VARCHAR(20) UNIQUE,
    first_name VARCHAR(100),
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth VARCHAR(20),
    gender VARCHAR(10),
    email VARCHAR(150),
    phone VARCHAR(20),
    address TEXT,
    guardian_first_name VARCHAR(100),
    guardian_middle_name VARCHAR(100),
    guardian_last_name VARCHAR(100),
    guardian_phone VARCHAR(20),
    guardian_relation VARCHAR(50),
    grade_level VARCHAR(20),
    strand VARCHAR(50),
    previous_school VARCHAR(200),
    school_year VARCHAR(20),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ── student_status ────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_lrn VARCHAR(20) UNIQUE,
    status VARCHAR(20) DEFAULT 'Pending',
    feedback TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_lrn) REFERENCES student_info(lrn_id)
)
""")

# ── student_credentials ───────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_lrn VARCHAR(20) UNIQUE,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    FOREIGN KEY (student_lrn) REFERENCES student_info(lrn_id)
)
""")

# ── staff_credentials ─────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    full_name VARCHAR(200),
    email VARCHAR(150),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ── admin_credentials ─────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    full_name VARCHAR(200),
    email VARCHAR(150),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ── announcements ─────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    target VARCHAR(20) DEFAULT 'both',
    posted_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ── class_schedule ────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS class_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    strand VARCHAR(50),
    grade_level VARCHAR(20),
    semester VARCHAR(10),
    subject VARCHAR(150),
    teacher VARCHAR(150),
    day_time VARCHAR(100),
    room VARCHAR(50)
)
""")

# ── student_grades ────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_lrn VARCHAR(20),
    subject VARCHAR(150),
    semester VARCHAR(10),
    grade DECIMAL(5,2),
    school_year VARCHAR(20),
    FOREIGN KEY (student_lrn) REFERENCES student_info(lrn_id)
)
""")

connection.commit()
print("✅ All tables created successfully.")

# ── Seed default admin account ────────────────────────────────
cursor.execute("SELECT * FROM admin_credentials WHERE username = 'admin'")
if not cursor.fetchone():
    hashed = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt()).decode()
    cursor.execute(
        "INSERT INTO admin_credentials (username, full_name, email, password) VALUES (%s,%s,%s,%s)",
        ('admin', 'System Administrator', 'admin@springfield.edu', hashed)
    )
    connection.commit()
    print("✅ Default admin created — username: admin / password: admin123")

# ── Seed sample class schedule ────────────────────────────────
cursor.execute("SELECT COUNT(*) FROM class_schedule")
count = cursor.fetchone()[0]
if count == 0:
    schedules = [
        # STEM Grade 11, Sem 1
        ('STEM', 'Grade 11', '1st', 'General Mathematics', 'Mr. Santos', 'Mon/Wed 7:30–9:00', 'Rm 101'),
        ('STEM', 'Grade 11', '1st', 'Earth Science', 'Ms. Cruz', 'Tue/Thu 7:30–9:00', 'Rm 102'),
        ('STEM', 'Grade 11', '1st', 'Oral Communication', 'Ms. Reyes', 'Mon/Wed 9:00–10:30', 'Rm 103'),
        ('STEM', 'Grade 11', '1st', 'Personal Development', 'Mr. Lim', 'Fri 7:30–10:30', 'Rm 104'),
        # STEM Grade 11, Sem 2
        ('STEM', 'Grade 11', '2nd', 'Pre-Calculus', 'Mr. Santos', 'Mon/Wed 7:30–9:00', 'Rm 101'),
        ('STEM', 'Grade 11', '2nd', 'Biology', 'Ms. Torres', 'Tue/Thu 7:30–9:00', 'Lab 1'),
        ('STEM', 'Grade 11', '2nd', 'Reading & Writing', 'Ms. Reyes', 'Mon/Wed 9:00–10:30', 'Rm 103'),
        # ABM Grade 11, Sem 1
        ('ABM', 'Grade 11', '1st', 'Business Math', 'Ms. Flores', 'Mon/Wed 7:30–9:00', 'Rm 201'),
        ('ABM', 'Grade 11', '1st', 'Organization & Management', 'Mr. Garcia', 'Tue/Thu 7:30–9:00', 'Rm 202'),
        ('ABM', 'Grade 11', '1st', 'Oral Communication', 'Ms. Reyes', 'Mon/Wed 9:00–10:30', 'Rm 103'),
        # HUMSS Grade 12, Sem 1
        ('HUMSS', 'Grade 12', '1st', 'Creative Writing', 'Ms. Mendoza', 'Mon/Wed 7:30–9:00', 'Rm 301'),
        ('HUMSS', 'Grade 12', '1st', 'Philippine Politics', 'Mr. Ramos', 'Tue/Thu 7:30–9:00', 'Rm 302'),
        ('HUMSS', 'Grade 12', '2nd', 'Disciplines in Social Sciences', 'Mr. Ramos', 'Mon/Wed 7:30–9:00', 'Rm 302'),
    ]
    cursor.executemany(
        "INSERT INTO class_schedule (strand,grade_level,semester,subject,teacher,day_time,room) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        schedules
    )
    connection.commit()
    print("✅ Sample schedules inserted.")

cursor.close()
connection.close()
print("\n🏫 Springfield Academy database is ready!")
