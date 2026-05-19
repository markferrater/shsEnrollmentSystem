import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QStackedWidget, QGroupBox, QMessageBox, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QTabWidget, QFrame, QGridLayout, QTextEdit, QDateEdit,
    QRadioButton, QButtonGroup, QCheckBox, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import QDate, QTimer


# ========================================================================
# DATA MODELS (Simulated Database)
# ========================================================================

class SchoolData:
    """Simulated database for the enrollment system"""

    # Student data storage
    students = [
        {
            'lrn': '123456789012',
            'first_name': 'Juan',
            'middle_name': 'Santos',
            'last_name': 'Dela Cruz',
            'birth_date': '2008-05-15',
            'gender': 'Male',
            'email': 'juan.delacruz@email.com',
            'phone': '09123456789',
            'guardian_first': 'Maria',
            'guardian_middle': 'Santos',
            'guardian_last': 'Dela Cruz',
            'guardian_phone': '09187654321',
            'relation': 'Mother',
            'grade_level': 'Grade 11',
            'strand': 'STEM',
            'semester': '1st Semester',
            'previous_school': 'Springfield National High School',
            'school_year': '2024-2025',
            'status': 'Enrolled'
        },
        {
            'lrn': '223456789013',
            'first_name': 'Maria',
            'middle_name': 'Gonzales',
            'last_name': 'Santos',
            'birth_date': '2007-11-20',
            'gender': 'Female',
            'email': 'maria.santos@email.com',
            'phone': '09234567890',
            'guardian_first': 'Pedro',
            'guardian_middle': 'Gonzales',
            'guardian_last': 'Santos',
            'guardian_phone': '09196543218',
            'relation': 'Father',
            'grade_level': 'Grade 12',
            'strand': 'ABM',
            'semester': '2nd Semester',
            'previous_school': 'Springfield National High School',
            'school_year': '2024-2025',
            'status': 'Enrolled'
        },
        {
            'lrn': '323456789014',
            'first_name': 'Jose',
            'middle_name': 'Reyes',
            'last_name': 'Mendoza',
            'birth_date': '2008-03-10',
            'gender': 'Male',
            'email': 'jose.mendoza@email.com',
            'phone': '09345678901',
            'guardian_first': 'Ana',
            'guardian_middle': 'Reyes',
            'guardian_last': 'Mendoza',
            'guardian_phone': '09215436789',
            'relation': 'Mother',
            'grade_level': 'Grade 11',
            'strand': 'HUMSS',
            'semester': '1st Semester',
            'previous_school': 'Springfield National High School',
            'school_year': '2024-2025',
            'status': 'Pending'
        }
    ]

    # User accounts
    users = [
        {'username': 'juan.cruz', 'password': 'student123', 'role': 'student', 'student_lrn': '123456789012'},
        {'username': 'maria.santos', 'password': 'student123', 'role': 'student', 'student_lrn': '223456789013'},
        {'username': 'jose.mendoza', 'password': 'student123', 'role': 'student', 'student_lrn': '323456789014'},
        {'username': 'staff', 'password': 'staff123', 'role': 'staff', 'name': 'Ms. Rodriguez'},
        {'username': 'admin', 'password': 'admin123', 'role': 'admin', 'name': 'Dr. Santos'}
    ]

    # Grades data
    grades = [
        {'lrn': '123456789012', 'subject': 'Mathematics', 'grade': 88, 'semester': '1st'},
        {'lrn': '123456789012', 'subject': 'Science', 'grade': 92, 'semester': '1st'},
        {'lrn': '123456789012', 'subject': 'English', 'grade': 85, 'semester': '1st'},
        {'lrn': '123456789012', 'subject': 'Filipino', 'grade': 90, 'semester': '1st'},
        {'lrn': '223456789013', 'subject': 'Mathematics', 'grade': 91, 'semester': '2nd'},
        {'lrn': '223456789013', 'subject': 'Science', 'grade': 87, 'semester': '2nd'},
    ]

    # Subjects offered
    subjects = [
        {'grade': 'Grade 11', 'strand': 'STEM', 'subject': 'Calculus', 'schedule': 'Mon/Wed 8:00-9:30'},
        {'grade': 'Grade 11', 'strand': 'STEM', 'subject': 'Physics', 'schedule': 'Mon/Wed 9:30-11:00'},
        {'grade': 'Grade 11', 'strand': 'STEM', 'subject': 'Chemistry', 'schedule': 'Tue/Thu 8:00-9:30'},
        {'grade': 'Grade 11', 'strand': 'STEM', 'subject': 'Biology', 'schedule': 'Tue/Thu 9:30-11:00'},
        {'grade': 'Grade 11', 'strand': 'ABM', 'subject': 'Accounting', 'schedule': 'Mon/Wed 8:00-9:30'},
        {'grade': 'Grade 11', 'strand': 'ABM', 'subject': 'Economics', 'schedule': 'Mon/Wed 9:30-11:00'},
        {'grade': 'Grade 11', 'strand': 'HUMSS', 'subject': 'Literature', 'schedule': 'Tue/Thu 8:00-9:30'},
        {'grade': 'Grade 11', 'strand': 'HUMSS', 'subject': 'Philosophy', 'schedule': 'Tue/Thu 9:30-11:00'},
    ]

    # Announcements
    announcements = [
        {'date': '2024-01-15', 'title': 'Enrollment for SY 2024-2025',
         'content': 'Enrollment is now open for Grade 11 and 12 students.'},
        {'date': '2024-01-10', 'title': 'School Calendar', 'content': 'Classes will start on June 3, 2024.'},
        {'date': '2024-01-05', 'title': 'Scholarship Opportunities',
         'content': 'Academic scholarships available for deserving students.'},
    ]

    @classmethod
    def authenticate(cls, username, password):
        """Check login credentials"""
        for user in cls.users:
            if user['username'].lower() == username.lower() and user['password'] == password:
                return user
        return None

    @classmethod
    def get_student_by_lrn(cls, lrn):
        """Get student info by LRN"""
        for student in cls.students:
            if student['lrn'] == lrn:
                return student
        return None

    @classmethod
    def get_student_by_username(cls, username):
        """Get student by username"""
        user = None
        for u in cls.users:
            if u['username'].lower() == username.lower():
                user = u
                break

        if user and user['role'] == 'student' and 'student_lrn' in user:
            return cls.get_student_by_lrn(user['student_lrn'])
        return None

    @classmethod
    def get_student_grades(cls, lrn):
        """Get grades for a student"""
        student_grades = []
        for grade in cls.grades:
            if grade['lrn'] == lrn:
                student_grades.append(grade)
        return student_grades

    @classmethod
    def get_student_subjects(cls, lrn):
        """Get subjects for a student based on grade and strand"""
        student = cls.get_student_by_lrn(lrn)
        if not student:
            return []

        student_subjects = []
        for subject in cls.subjects:
            if (subject['grade'] == student['grade_level'] and
                    subject['strand'] == student['strand']):
                student_subjects.append(subject)
        return student_subjects

    @classmethod
    def add_student(cls, student_data):
        """Add new student"""
        # Generate new LRN if not provided
        if not student_data.get('lrn'):
            student_data['lrn'] = str(len(cls.students) + 1).zfill(12)

        # Set default status
        student_data['status'] = 'Pending'

        cls.students.append(student_data)

        # Create user account
        username = f"{student_data['first_name'].lower()}.{student_data['last_name'].lower()}"
        cls.users.append({
            'username': username,
            'password': 'student123',
            'role': 'student',
            'student_lrn': student_data['lrn']
        })

        return student_data['lrn'], username

    @classmethod
    def get_all_students(cls):
        """Get all students"""
        return cls.students

    @classmethod
    def update_student_status(cls, lrn, status):
        """Update student enrollment status"""
        for student in cls.students:
            if student['lrn'] == lrn:
                student['status'] = status
                return True
        return False

    @classmethod
    def get_statistics(cls):
        """Get enrollment statistics"""
        total = len(cls.students)
        enrolled = sum(1 for s in cls.students if s['status'] == 'Enrolled')
        pending = sum(1 for s in cls.students if s['status'] == 'Pending')

        grade11 = sum(1 for s in cls.students if s['grade_level'] == 'Grade 11')
        grade12 = sum(1 for s in cls.students if s['grade_level'] == 'Grade 12')

        stem = sum(1 for s in cls.students if s['strand'] == 'STEM')
        abm = sum(1 for s in cls.students if s['strand'] == 'ABM')
        humss = sum(1 for s in cls.students if s['strand'] == 'HUMSS')

        return {
            'total': total,
            'enrolled': enrolled,
            'pending': pending,
            'grade11': grade11,
            'grade12': grade12,
            'stem': stem,
            'abm': abm,
            'humss': humss
        }


# ========================================================================
# STYLESHEETS
# ========================================================================

class Styles:
    MAIN_WINDOW = """
        QMainWindow {
            background-color: #f5f6fa;
        }
    """

    LOGIN_BOX = """
        QWidget {
            background-color: white;
            border-radius: 15px;
        }
    """

    LOGIN_CARD = """
        QWidget {
            background-color: #3498db;
            border-radius: 10px;
            color: white;
        }
        QWidget:hover {
            background-color: #2980b9;
            border: 2px solid #f1c40f;
        }
        QLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton {
            background-color: #2c3e50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #34495e;
        }
    """

    BUTTON_PRIMARY = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1c6ea9;
        }
    """

    BUTTON_SUCCESS = """
        QPushButton {
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #2ecc71;
        }
    """

    BUTTON_DANGER = """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
    """

    SIDEBAR = """
        QWidget {
            background-color: #2c3e50;
        }
        QPushButton {
            background-color: transparent;
            color: white;
            border: none;
            text-align: left;
            padding: 15px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #34495e;
            border-left: 4px solid #3498db;
        }
        QPushButton:checked {
            background-color: #3498db;
            border-left: 4px solid #f1c40f;
        }
        QLabel {
            color: white;
        }
    """

    CARD = """
        QFrame {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
        }
    """

    TABLE = """
        QTableWidget {
            background-color: white;
            border: none;
            border-radius: 5px;
            gridline-color: #ecf0f1;
        }
        QHeaderView::section {
            background-color: #3498db;
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
    """

    INPUT = """
        QLineEdit, QComboBox, QDateEdit, QSpinBox {
            border: 1px solid #dcdde1;
            border-radius: 5px;
            padding: 8px;
            background-color: white;
        }
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 2px solid #3498db;
        }
    """

    GROUPBOX = """
        QGroupBox {
            font-weight: bold;
            border: 2px solid #3498db;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #3498db;
        }
    """


# ========================================================================
# LOGIN PAGE
# ========================================================================

class LoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # School logo and name
        title_label = QLabel("🏫 SPRINGFIELD ACADEMY")
        title_label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Senior High School Enrollment System")
        subtitle.setStyleSheet("""
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 40px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login cards container
        cards_widget = QWidget()
        cards_widget.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 30px;
        """)
        cards_layout = QHBoxLayout(cards_widget)
        cards_layout.setSpacing(30)

        # Student Login Card
        student_card = self.create_login_card(
            "🎓",
            "Student Portal",
            "Access your grades, subjects, and enrollment status",
            "#3498db"
        )
        student_btn = student_card.findChild(QPushButton)
        student_btn.clicked.connect(lambda: self.go_to_login('student'))

        # Staff Login Card
        staff_card = self.create_login_card(
            "👥",
            "Staff Portal",
            "Manage student enrollment and records",
            "#27ae60"
        )
        staff_btn = staff_card.findChild(QPushButton)
        staff_btn.clicked.connect(lambda: self.go_to_login('staff'))

        # Admin Login Card
        admin_card = self.create_login_card(
            "👑",
            "Admin Portal",
            "System administration and user management",
            "#e74c3c"
        )
        admin_btn = admin_card.findChild(QPushButton)
        admin_btn.clicked.connect(lambda: self.go_to_login('admin'))

        cards_layout.addWidget(student_card)
        cards_layout.addWidget(staff_card)
        cards_layout.addWidget(admin_card)

        # Footer
        footer = QLabel("© 2024 Springfield Academy. All rights reserved.")
        footer.setStyleSheet("color: #95a5a6; margin-top: 30px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(cards_widget)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def create_login_card(self, emoji, title, description, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 15px;
                padding: 30px;
                min-width: 200px;
            }}
            QFrame:hover {{
                transform: scale(1.05);
                border: 3px solid #f1c40f;
            }}
            QLabel {{
                color: white;
            }}
        """)

        layout = QVBoxLayout(card)

        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 48px;")
        emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 12px; margin: 10px 0;")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)

        layout.addWidget(emoji_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(login_btn)

        return card

    def go_to_login(self, portal_type):
        if portal_type == 'student':
            self.stack.setCurrentIndex(1)
        elif portal_type == 'staff':
            self.stack.setCurrentIndex(5)
        elif portal_type == 'admin':
            self.stack.setCurrentIndex(7)


# ========================================================================
# STUDENT LOGIN PAGE
# ========================================================================

class StudentLoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login box
        login_box = QFrame()
        login_box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 40px;
                max-width: 400px;
            }
        """)
        login_layout = QVBoxLayout(login_box)

        # Back button
        back_btn = QPushButton("← Back to Portal Selection")
        back_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #3498db;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        # Title
        title = QLabel("🎓 Student Login")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin: 20px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Username
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username (e.g., juan.cruz)")
        self.username_input.setStyleSheet(Styles.INPUT)

        # Password
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(Styles.INPUT)

        # Show password checkbox
        self.show_password = QCheckBox("Show Password")
        self.show_password.stateChanged.connect(self.toggle_password)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(Styles.BUTTON_PRIMARY)
        login_btn.clicked.connect(self.login)

        # Register link
        register_label = QLabel("Don't have an account?")
        register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        register_btn = QPushButton("Register as New Student")
        register_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #3498db;
                font-weight: bold;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        register_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        # Demo credentials
        demo_box = QFrame()
        demo_box.setStyleSheet("background-color: #f8f9fa; border-radius: 5px; padding: 10px; margin-top: 20px;")
        demo_layout = QVBoxLayout(demo_box)
        demo_layout.addWidget(QLabel("Demo Credentials:"))
        demo_layout.addWidget(QLabel("Username: juan.cruz"))
        demo_layout.addWidget(QLabel("Password: student123"))

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.show_password)
        form_layout.addWidget(login_btn)
        form_layout.addWidget(register_label)
        form_layout.addWidget(register_btn)
        form_layout.addWidget(demo_box)

        login_layout.addWidget(back_btn)
        login_layout.addWidget(title)
        login_layout.addLayout(form_layout)

        main_layout.addWidget(login_box)
        self.setLayout(main_layout)

    def toggle_password(self):
        if self.show_password.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter username and password")
            return

        user = SchoolData.authenticate(username, password)

        if user and user['role'] == 'student':
            self.username_input.clear()
            self.password_input.clear()
            # Store current user
            self.stack.parent().current_user = user
            self.stack.setCurrentIndex(2)  # Go to student dashboard
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")


# ========================================================================
# STUDENT DASHBOARD
# ========================================================================

class StudentDashboard(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.current_user = None

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = self.create_sidebar()

        # Content area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #f5f6fa;")

        # Create pages
        self.dashboard_page = self.create_dashboard_page()
        self.grades_page = self.create_grades_page()
        self.subjects_page = self.create_subjects_page()
        self.profile_page = self.create_profile_page()

        self.content_stack.addWidget(self.dashboard_page)  # index 0
        self.content_stack.addWidget(self.grades_page)  # index 1
        self.content_stack.addWidget(self.subjects_page)  # index 2
        self.content_stack.addWidget(self.profile_page)  # index 3

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack, 1)

        self.setLayout(main_layout)

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet(Styles.SIDEBAR)

        layout = QVBoxLayout(sidebar)
        layout.setSpacing(10)

        # School logo
        logo_label = QLabel("🏫\nSpringfield\nAcademy")
        logo_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Navigation buttons
        self.dash_btn = QPushButton("🏠 Dashboard")
        self.dash_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.dash_btn.setCheckable(True)
        self.dash_btn.setChecked(True)

        self.grades_btn = QPushButton("📊 My Grades")
        self.grades_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        self.grades_btn.setCheckable(True)

        self.subjects_btn = QPushButton("📚 My Subjects")
        self.subjects_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))
        self.subjects_btn.setCheckable(True)

        self.profile_btn = QPushButton("👤 My Profile")
        self.profile_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(3))
        self.profile_btn.setCheckable(True)

        layout.addWidget(self.dash_btn)
        layout.addWidget(self.grades_btn)
        layout.addWidget(self.subjects_btn)
        layout.addWidget(self.profile_btn)
        layout.addStretch()

        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        return sidebar

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Welcome banner
        banner = QFrame()
        banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 10px;
                color: white;
                padding: 20px;
            }
        """)
        banner_layout = QHBoxLayout(banner)

        self.welcome_label = QLabel("Welcome back, Student!")
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        date_label = QLabel(QDate.currentDate().toString("dddd, MMMM d, yyyy"))
        date_label.setStyleSheet("font-size: 14px; opacity: 0.9;")

        banner_layout.addWidget(self.welcome_label)
        banner_layout.addStretch()
        banner_layout.addWidget(date_label)

        layout.addWidget(banner)

        # Stats cards
        stats_layout = QHBoxLayout()

        stats_data = [
            ("📊", "GPA", "89.5"),
            ("📚", "Subjects", "8"),
            ("📝", "Attendance", "95%"),
        ]

        for icon, label, value in stats_data:
            card = QFrame()
            card.setStyleSheet(Styles.CARD)
            card_layout = QVBoxLayout(card)

            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 32px;")

            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")

            name_label = QLabel(label)
            name_label.setStyleSheet("color: #7f8c8d;")

            card_layout.addWidget(icon_label)
            card_layout.addWidget(value_label)
            card_layout.addWidget(name_label)

            stats_layout.addWidget(card)

        layout.addLayout(stats_layout)

        # Recent announcements
        announcements_group = QGroupBox("Recent Announcements")
        announcements_group.setStyleSheet(Styles.GROUPBOX)
        announcements_layout = QVBoxLayout(announcements_group)

        for announcement in SchoolData.announcements[:3]:
            ann_frame = QFrame()
            ann_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 5px; padding: 10px; margin: 5px;")
            ann_layout = QVBoxLayout(ann_frame)

            title_label = QLabel(f"📢 {announcement['title']}")
            title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

            date_label = QLabel(announcement['date'])
            date_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")

            content_label = QLabel(announcement['content'])
            content_label.setWordWrap(True)

            ann_layout.addWidget(title_label)
            ann_layout.addWidget(date_label)
            ann_layout.addWidget(content_label)

            announcements_layout.addWidget(ann_frame)

        layout.addWidget(announcements_group)
        layout.addStretch()

        return page

    def create_grades_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("📊 My Grades")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)

        # Semester selector
        semester_layout = QHBoxLayout()
        semester_layout.addWidget(QLabel("Select Semester:"))
        self.semester_combo = QComboBox()
        self.semester_combo.addItems(["1st Semester", "2nd Semester"])
        self.semester_combo.setStyleSheet(Styles.INPUT)
        self.semester_combo.currentTextChanged.connect(self.load_grades)
        semester_layout.addWidget(self.semester_combo)
        semester_layout.addStretch()
        layout.addLayout(semester_layout)

        # Grades table
        self.grades_table = QTableWidget()
        self.grades_table.setColumnCount(3)
        self.grades_table.setHorizontalHeaderLabels(["Subject", "Grade", "Remarks"])
        self.grades_table.setStyleSheet(Styles.TABLE)
        self.grades_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.grades_table)

        # Summary
        summary_frame = QFrame()
        summary_frame.setStyleSheet(Styles.CARD)
        summary_layout = QHBoxLayout(summary_frame)

        self.gpa_label = QLabel("GPA: --")
        self.gpa_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")

        self.remarks_label = QLabel("Remarks: --")
        self.remarks_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")

        summary_layout.addWidget(self.gpa_label)
        summary_layout.addWidget(self.remarks_label)
        summary_layout.addStretch()

        layout.addWidget(summary_frame)

        return page

    def create_subjects_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("📚 My Subjects")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)

        # Subjects table
        self.subjects_table = QTableWidget()
        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels(["Subject", "Schedule", "Room"])
        self.subjects_table.setStyleSheet(Styles.TABLE)
        self.subjects_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.subjects_table)

        return page

    def create_profile_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("👤 My Profile")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)

        # Profile info
        self.profile_frame = QFrame()
        self.profile_frame.setStyleSheet(Styles.CARD)
        profile_layout = QGridLayout(self.profile_frame)
        profile_layout.setVerticalSpacing(15)
        profile_layout.setHorizontalSpacing(30)

        # Personal Information
        personal_group = QGroupBox("Personal Information")
        personal_group.setStyleSheet(Styles.GROUPBOX)
        personal_layout = QGridLayout(personal_group)

        self.personal_labels = {}
        fields = [
            ("LRN:", "lrn"), ("Name:", "name"), ("Birth Date:", "birth"),
            ("Gender:", "gender"), ("Email:", "email"), ("Phone:", "phone")
        ]

        for i, (label, key) in enumerate(fields):
            personal_layout.addWidget(QLabel(label), i, 0)
            value_label = QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            personal_layout.addWidget(value_label, i, 1)
            self.personal_labels[key] = value_label

        # Guardian Information
        guardian_group = QGroupBox("Guardian Information")
        guardian_group.setStyleSheet(Styles.GROUPBOX)
        guardian_layout = QGridLayout(guardian_group)

        guardian_fields = [
            ("Guardian:", "guardian_name"), ("Contact:", "guardian_phone"),
            ("Relation:", "relation")
        ]

        for i, (label, key) in enumerate(guardian_fields):
            guardian_layout.addWidget(QLabel(label), i, 0)
            value_label = QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            guardian_layout.addWidget(value_label, i, 1)
            self.personal_labels[key] = value_label

        # Academic Information
        academic_group = QGroupBox("Academic Information")
        academic_group.setStyleSheet(Styles.GROUPBOX)
        academic_layout = QGridLayout(academic_group)

        academic_fields = [
            ("Grade Level:", "grade"), ("Strand:", "strand"),
            ("Semester:", "semester"), ("School Year:", "school_year"),
            ("Status:", "status")
        ]

        for i, (label, key) in enumerate(academic_fields):
            academic_layout.addWidget(QLabel(label), i, 0)
            value_label = QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            academic_layout.addWidget(value_label, i, 1)
            self.personal_labels[key] = value_label

        profile_layout.addWidget(personal_group, 0, 0)
        profile_layout.addWidget(guardian_group, 0, 1)
        profile_layout.addWidget(academic_group, 1, 0, 1, 2)

        layout.addWidget(self.profile_frame)
        layout.addStretch()

        return page

    def load_student_data(self):
        """Load student data into dashboard"""
        if not self.stack.parent().current_user:
            return

        user = self.stack.parent().current_user
        student = SchoolData.get_student_by_username(user['username'])

        if not student:
            return

        # Update welcome message
        self.welcome_label.setText(f"Welcome back, {student['first_name']} {student['last_name']}!")

        # Update profile page
        self.personal_labels['lrn'].setText(student['lrn'])
        self.personal_labels['name'].setText(f"{student['first_name']} {student['middle_name']} {student['last_name']}")
        self.personal_labels['birth'].setText(student['birth_date'])
        self.personal_labels['gender'].setText(student['gender'])
        self.personal_labels['email'].setText(student['email'])
        self.personal_labels['phone'].setText(student['phone'])

        self.personal_labels['guardian_name'].setText(
            f"{student['guardian_first']} {student['guardian_middle']} {student['guardian_last']}")
        self.personal_labels['guardian_phone'].setText(student['guardian_phone'])
        self.personal_labels['relation'].setText(student['relation'])

        self.personal_labels['grade'].setText(student['grade_level'])
        self.personal_labels['strand'].setText(student['strand'])
        self.personal_labels['semester'].setText(student['semester'])
        self.personal_labels['school_year'].setText(student['school_year'])
        self.personal_labels['status'].setText(student['status'])

        # Load grades
        self.load_grades()

        # Load subjects
        self.load_subjects()

    def load_grades(self):
        """Load student grades"""
        if not self.stack.parent().current_user:
            return

        user = self.stack.parent().current_user
        student = SchoolData.get_student_by_username(user['username'])

        if not student:
            return

        grades = SchoolData.get_student_grades(student['lrn'])
        semester = self.semester_combo.currentText().split()[0].lower()

        filtered_grades = [g for g in grades if g['semester'] == semester]

        self.grades_table.setRowCount(len(filtered_grades))

        total = 0
        for i, grade in enumerate(filtered_grades):
            self.grades_table.setItem(i, 0, QTableWidgetItem(grade['subject']))
            self.grades_table.setItem(i, 1, QTableWidgetItem(str(grade['grade'])))

            remarks = "Passed" if grade['grade'] >= 75 else "Failed"
            if grade['grade'] >= 90:
                remarks = "Excellent"
            elif grade['grade'] >= 85:
                remarks = "Very Good"
            elif grade['grade'] >= 80:
                remarks = "Good"
            elif grade['grade'] >= 75:
                remarks = "Fair"

            self.grades_table.setItem(i, 2, QTableWidgetItem(remarks))
            total += grade['grade']

        if filtered_grades:
            gpa = total / len(filtered_grades)
            self.gpa_label.setText(f"GPA: {gpa:.2f}")
            self.remarks_label.setText(f"Remarks: {'Passed' if gpa >= 75 else 'Failed'}")

    def load_subjects(self):
        """Load student subjects"""
        if not self.stack.parent().current_user:
            return

        user = self.stack.parent().current_user
        student = SchoolData.get_student_by_username(user['username'])

        if not student:
            return

        subjects = SchoolData.get_student_subjects(student['lrn'])

        self.subjects_table.setRowCount(len(subjects))

        rooms = ['Room 101', 'Room 102', 'Room 103', 'Room 104', 'Lab A', 'Lab B']
        for i, subject in enumerate(subjects):
            self.subjects_table.setItem(i, 0, QTableWidgetItem(subject['subject']))
            self.subjects_table.setItem(i, 1, QTableWidgetItem(subject['schedule']))
            self.subjects_table.setItem(i, 2, QTableWidgetItem(rooms[i % len(rooms)]))

    def showEvent(self, event):
        """Called when widget is shown"""
        super().showEvent(event)
        self.load_student_data()

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.stack.setCurrentIndex(0)


# ========================================================================
# STUDENT REGISTRATION FORM
# ========================================================================

class StudentRegistrationPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #2c3e50; color: white; padding: 20px;")
        header_layout = QHBoxLayout(header)

        back_btn = QPushButton("← Back to Login")
        back_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        title = QLabel("Student Enrollment Form")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        header_layout.addWidget(back_btn)
        header_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #f5f6fa;")

        # Form container
        container = QWidget()
        container.setStyleSheet("background-color: white; border-radius: 10px;")
        form_layout = QVBoxLayout(container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Personal Information
        personal_group = QGroupBox("Personal Information")
        personal_group.setStyleSheet(Styles.GROUPBOX)
        personal_layout = QGridLayout(personal_group)
        personal_layout.setVerticalSpacing(15)
        personal_layout.setHorizontalSpacing(20)

        # Row 1: Name fields
        personal_layout.addWidget(QLabel("First Name:*"), 0, 0)
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        self.first_name.setStyleSheet(Styles.INPUT)
        personal_layout.addWidget(self.first_name, 0, 1)

        personal_layout.addWidget(QLabel("Middle Name:"), 0, 2)
        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Middle Name")
        self.middle_name.setStyleSheet(Styles.INPUT)
        personal_layout.addWidget(self.middle_name, 0, 3)

        personal_layout.addWidget(QLabel("Last Name:*"), 0, 4)
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")
        self.last_name.setStyleSheet(Styles.INPUT)
        personal_layout.addWidget(self.last_name, 0, 5)

        # Row 2: Birth Date and Gender
        personal_layout.addWidget(QLabel("Birth Date:*"), 1, 0)
        self.birth_date = QDateEdit()
        self.birth_date.setDate(QDate.currentDate().addYears(-15))
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setDisplayFormat("yyyy-MM-dd")
        self.birth_date.setStyleSheet(Styles.INPUT)
        personal_layout.addWidget(self.birth_date, 1, 1)

        personal_layout.addWidget(QLabel("Gender:*"), 1, 2)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setStyleSheet(Styles.INPUT)
        personal_layout.addWidget(self.gender_combo, 1, 3)

        # Contact Information
        contact_group = QGroupBox("Contact Information")
        contact_group.setStyleSheet(Styles.GROUPBOX)
        contact_layout = QGridLayout(contact_group)
        contact_layout.setVerticalSpacing(15)
        contact_layout.setHorizontalSpacing(20)

        contact_layout.addWidget(QLabel("Email:*"), 0, 0)
        self.email = QLineEdit()
        self.email.setPlaceholderText("email@example.com")
        self.email.setStyleSheet(Styles.INPUT)
        contact_layout.addWidget(self.email, 0, 1)

        contact_layout.addWidget(QLabel("Phone:*"), 0, 2)
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("09123456789")
        self.phone.setStyleSheet(Styles.INPUT)
        contact_layout.addWidget(self.phone, 0, 3)

        # Guardian Information
        guardian_group = QGroupBox("Guardian Information")
        guardian_group.setStyleSheet(Styles.GROUPBOX)
        guardian_layout = QGridLayout(guardian_group)
        guardian_layout.setVerticalSpacing(15)
        guardian_layout.setHorizontalSpacing(20)

        # Guardian Name
        guardian_layout.addWidget(QLabel("Guardian First Name:*"), 0, 0)
        self.guardian_first = QLineEdit()
        self.guardian_first.setPlaceholderText("First Name")
        self.guardian_first.setStyleSheet(Styles.INPUT)
        guardian_layout.addWidget(self.guardian_first, 0, 1)

        guardian_layout.addWidget(QLabel("Middle Name:"), 0, 2)
        self.guardian_middle = QLineEdit()
        self.guardian_middle.setPlaceholderText("Middle Name")
        self.guardian_middle.setStyleSheet(Styles.INPUT)
        guardian_layout.addWidget(self.guardian_middle, 0, 3)

        guardian_layout.addWidget(QLabel("Last Name:*"), 0, 4)
        self.guardian_last = QLineEdit()
        self.guardian_last.setPlaceholderText("Last Name")
        self.guardian_last.setStyleSheet(Styles.INPUT)
        guardian_layout.addWidget(self.guardian_last, 0, 5)

        # Guardian Contact
        guardian_layout.addWidget(QLabel("Guardian Phone:*"), 1, 0)
        self.guardian_phone = QLineEdit()
        self.guardian_phone.setPlaceholderText("09123456789")
        self.guardian_phone.setStyleSheet(Styles.INPUT)
        guardian_layout.addWidget(self.guardian_phone, 1, 1)

        guardian_layout.addWidget(QLabel("Relationship:*"), 1, 2)
        self.relation = QComboBox()
        self.relation.addItems(["Father", "Mother", "Guardian", "Other"])
        self.relation.setStyleSheet(Styles.INPUT)
        guardian_layout.addWidget(self.relation, 1, 3)

        # Academic Information
        academic_group = QGroupBox("Academic Information")
        academic_group.setStyleSheet(Styles.GROUPBOX)
        academic_layout = QGridLayout(academic_group)
        academic_layout.setVerticalSpacing(15)
        academic_layout.setHorizontalSpacing(20)

        academic_layout.addWidget(QLabel("Grade Level:*"), 0, 0)
        self.grade_level = QComboBox()
        self.grade_level.addItems(["Grade 11", "Grade 12"])
        self.grade_level.setStyleSheet(Styles.INPUT)
        academic_layout.addWidget(self.grade_level, 0, 1)

        academic_layout.addWidget(QLabel("Strand:*"), 0, 2)
        self.strand = QComboBox()
        self.strand.addItems(["STEM", "ABM", "HUMSS", "GAS", "TVL"])
        self.strand.setStyleSheet(Styles.INPUT)
        academic_layout.addWidget(self.strand, 0, 3)

        academic_layout.addWidget(QLabel("Semester:*"), 0, 4)
        self.semester = QComboBox()
        self.semester.addItems(["1st Semester", "2nd Semester"])
        self.semester.setStyleSheet(Styles.INPUT)
        academic_layout.addWidget(self.semester, 0, 5)

        academic_layout.addWidget(QLabel("School Year:*"), 1, 0)
        self.school_year = QLineEdit()
        self.school_year.setText("2024-2025")
        self.school_year.setStyleSheet(Styles.INPUT)
        academic_layout.addWidget(self.school_year, 1, 1)

        academic_layout.addWidget(QLabel("Previous School:"), 1, 2)
        self.prev_school = QLineEdit()
        self.prev_school.setPlaceholderText("Previous School Name")
        self.prev_school.setStyleSheet(Styles.INPUT)
        academic_layout.addWidget(self.prev_school, 1, 3, 1, 2)

        # Submit button
        submit_btn = QPushButton("Submit Enrollment")
        submit_btn.setStyleSheet(Styles.BUTTON_SUCCESS + "font-size: 16px; padding: 15px;")
        submit_btn.clicked.connect(self.submit_form)

        # Required fields note
        note_label = QLabel("* Required fields")
        note_label.setStyleSheet("color: #e74c3c; font-style: italic;")

        # Add all groups to form
        form_layout.addWidget(personal_group)
        form_layout.addWidget(contact_group)
        form_layout.addWidget(guardian_group)
        form_layout.addWidget(academic_group)
        form_layout.addWidget(note_label)
        form_layout.addWidget(submit_btn)

        scroll.setWidget(container)

        main_layout.addWidget(header)
        main_layout.addWidget(scroll, 1)

        self.setLayout(main_layout)

    def submit_form(self):
        # Validate required fields
        if not self.first_name.text():
            QMessageBox.warning(self, "Validation Error", "First name is required")
            return
        if not self.last_name.text():
            QMessageBox.warning(self, "Validation Error", "Last name is required")
            return
        if not self.email.text():
            QMessageBox.warning(self, "Validation Error", "Email is required")
            return
        if not self.phone.text():
            QMessageBox.warning(self, "Validation Error", "Phone number is required")
            return
        if not self.guardian_first.text():
            QMessageBox.warning(self, "Validation Error", "Guardian first name is required")
            return
        if not self.guardian_last.text():
            QMessageBox.warning(self, "Validation Error", "Guardian last name is required")
            return
        if not self.guardian_phone.text():
            QMessageBox.warning(self, "Validation Error", "Guardian phone is required")
            return

        # Create student data
        student_data = {
            'first_name': self.first_name.text(),
            'middle_name': self.middle_name.text(),
            'last_name': self.last_name.text(),
            'birth_date': self.birth_date.date().toString("yyyy-MM-dd"),
            'gender': self.gender_combo.currentText(),
            'email': self.email.text(),
            'phone': self.phone.text(),
            'guardian_first': self.guardian_first.text(),
            'guardian_middle': self.guardian_middle.text(),
            'guardian_last': self.guardian_last.text(),
            'guardian_phone': self.guardian_phone.text(),
            'relation': self.relation.currentText(),
            'grade_level': self.grade_level.currentText(),
            'strand': self.strand.currentText(),
            'semester': self.semester.currentText(),
            'school_year': self.school_year.text(),
            'previous_school': self.prev_school.text() or "N/A"
        }

        # Add to database
        lrn, username = SchoolData.add_student(student_data)

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Registration Successful")
        msg.setText(f"Student enrolled successfully!\n\nLRN: {lrn}\nUsername: {username}\nPassword: student123")
        msg.setInformativeText("Please save these credentials for login.")
        msg.exec()

        # Clear form
        self.clear_form()

        # Go back to login
        self.stack.setCurrentIndex(1)

    def clear_form(self):
        self.first_name.clear()
        self.middle_name.clear()
        self.last_name.clear()
        self.email.clear()
        self.phone.clear()
        self.guardian_first.clear()
        self.guardian_middle.clear()
        self.guardian_last.clear()
        self.guardian_phone.clear()
        self.prev_school.clear()


# ========================================================================
# STAFF LOGIN PAGE
# ========================================================================

class StaffLoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_box = QFrame()
        login_box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 40px;
                max-width: 400px;
            }
        """)
        login_layout = QVBoxLayout(login_box)

        # Back button
        back_btn = QPushButton("← Back to Portal Selection")
        back_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #27ae60;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        # Title
        title = QLabel("👥 Staff Login")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #27ae60; margin: 20px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter staff username")
        self.username_input.setStyleSheet(Styles.INPUT)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(Styles.INPUT)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(Styles.BUTTON_SUCCESS)
        login_btn.clicked.connect(self.login)

        # Demo credentials
        demo_box = QFrame()
        demo_box.setStyleSheet("background-color: #f8f9fa; border-radius: 5px; padding: 10px; margin-top: 20px;")
        demo_layout = QVBoxLayout(demo_box)
        demo_layout.addWidget(QLabel("Demo Credentials:"))
        demo_layout.addWidget(QLabel("Username: staff"))
        demo_layout.addWidget(QLabel("Password: staff123"))

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_btn)
        form_layout.addWidget(demo_box)

        login_layout.addWidget(back_btn)
        login_layout.addWidget(title)
        login_layout.addLayout(form_layout)

        main_layout.addWidget(login_box)
        self.setLayout(main_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter username and password")
            return

        user = SchoolData.authenticate(username, password)

        if user and user['role'] == 'staff':
            self.username_input.clear()
            self.password_input.clear()
            self.stack.parent().current_user = user
            self.stack.setCurrentIndex(6)  # Go to staff dashboard
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")


# ========================================================================
# STAFF DASHBOARD
# ========================================================================

class StaffDashboard(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #27ae60; color: white; padding: 15px;")
        header_layout = QHBoxLayout(header)

        title = QLabel("Staff Dashboard - Enrollment Management")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.user_label = QLabel("Welcome, Staff")
        self.user_label.setStyleSheet("font-size: 14px;")

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.logout)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.user_label)
        header_layout.addWidget(logout_btn)

        # Content area with tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #f5f6fa;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 10px 20px;
                background-color: #ecf0f1;
                border: none;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #27ae60;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #2ecc71;
                color: white;
            }
        """)

        # Student Management Tab
        self.students_tab = self.create_students_tab()

        # Enrollment Requests Tab
        self.requests_tab = self.create_requests_tab()

        # Reports Tab
        self.reports_tab = self.create_reports_tab()

        self.tabs.addTab(self.students_tab, "📋 Student Management")
        self.tabs.addTab(self.requests_tab, "📝 Enrollment Requests")
        self.tabs.addTab(self.reports_tab, "📊 Reports")

        main_layout.addWidget(header)
        main_layout.addWidget(self.tabs, 1)

        self.setLayout(main_layout)
        self.load_students()

    def create_students_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, LRN, or strand...")
        self.search_input.setStyleSheet(Styles.INPUT)
        self.search_input.textChanged.connect(self.filter_students)

        search_btn = QPushButton("🔍 Search")
        search_btn.setStyleSheet(Styles.BUTTON_PRIMARY)
        search_btn.clicked.connect(self.filter_students)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(Styles.BUTTON_SUCCESS)
        refresh_btn.clicked.connect(self.load_students)

        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(refresh_btn)
        search_layout.addStretch()

        # Filter by strand
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by Strand:"))
        self.strand_filter = QComboBox()
        self.strand_filter.addItems(["All", "STEM", "ABM", "HUMSS", "GAS", "TVL"])
        self.strand_filter.setStyleSheet(Styles.INPUT)
        self.strand_filter.currentTextChanged.connect(self.filter_students)

        filter_layout.addWidget(self.strand_filter)
        filter_layout.addStretch()

        # Students table
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(8)
        self.students_table.setHorizontalHeaderLabels([
            "LRN", "Name", "Grade Level", "Strand", "Email", "Phone", "Status", "Actions"
        ])
        self.students_table.setStyleSheet(Styles.TABLE)
        self.students_table.horizontalHeader().setStretchLastSection(True)
        self.students_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addLayout(search_layout)
        layout.addLayout(filter_layout)
        layout.addWidget(self.students_table)

        return tab

    def create_requests_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Requests table
        self.requests_table = QTableWidget()
        self.requests_table.setColumnCount(7)
        self.requests_table.setHorizontalHeaderLabels([
            "LRN", "Name", "Grade Level", "Strand", "Date Applied", "Status", "Actions"
        ])
        self.requests_table.setStyleSheet(Styles.TABLE)
        self.requests_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.requests_table)
        self.load_requests()

        return tab

    def create_reports_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Statistics cards
        stats_layout = QHBoxLayout()

        stats = SchoolData.get_statistics()

        stat_cards = [
            ("Total Students", str(stats['total']), "#3498db"),
            ("Enrolled", str(stats['enrolled']), "#27ae60"),
            ("Pending", str(stats['pending']), "#e74c3c"),
            ("Grade 11", str(stats['grade11']), "#f39c12"),
            ("Grade 12", str(stats['grade12']), "#9b59b6"),
        ]

        for label, value, color in stat_cards:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 10px;
                    padding: 20px;
                    color: white;
                }}
            """)
            card_layout = QVBoxLayout(card)

            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 32px; font-weight: bold;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            name_label = QLabel(label)
            name_label.setStyleSheet("font-size: 14px;")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(value_label)
            card_layout.addWidget(name_label)
            stats_layout.addWidget(card)

        layout.addLayout(stats_layout)

        # Strand distribution
        strand_group = QGroupBox("Strand Distribution")
        strand_group.setStyleSheet(Styles.GROUPBOX)
        strand_layout = QVBoxLayout(strand_group)

        for strand in ["STEM", "ABM", "HUMSS"]:
            count = stats[strand.lower()]
            percent = (count / stats['total'] * 100) if stats['total'] > 0 else 0

            strand_item = QWidget()
            item_layout = QHBoxLayout(strand_item)
            item_layout.addWidget(QLabel(f"{strand}:"))
            item_layout.addWidget(QLabel(f"{count} students"))
            item_layout.addWidget(QLabel(f"({percent:.1f}%)"))

            strand_layout.addWidget(strand_item)

        layout.addWidget(strand_group)
        layout.addStretch()

        return tab

    def load_students(self):
        students = SchoolData.get_all_students()
        self.all_students = students
        self.display_students(students)
        self.load_requests()

    def display_students(self, students):
        self.students_table.setRowCount(len(students))

        for row, student in enumerate(students):
            self.students_table.setItem(row, 0, QTableWidgetItem(student['lrn']))
            name = f"{student['first_name']} {student['last_name']}"
            self.students_table.setItem(row, 1, QTableWidgetItem(name))
            self.students_table.setItem(row, 2, QTableWidgetItem(student['grade_level']))
            self.students_table.setItem(row, 3, QTableWidgetItem(student['strand']))
            self.students_table.setItem(row, 4, QTableWidgetItem(student['email']))
            self.students_table.setItem(row, 5, QTableWidgetItem(student['phone']))

            status_item = QTableWidgetItem(student['status'])
            if student['status'] == 'Enrolled':
                status_item.setForeground(QColor('#27ae60'))
            else:
                status_item.setForeground(QColor('#e74c3c'))
            self.students_table.setItem(row, 6, status_item)

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)

            if student['status'] == 'Pending':
                approve_btn = QPushButton("✓ Approve")
                approve_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #27ae60;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 3px 8px;
                    }
                    QPushButton:hover {
                        background-color: #2ecc71;
                    }
                """)
                approve_btn.clicked.connect(lambda checked, lrn=student['lrn']: self.approve_student(lrn))
                action_layout.addWidget(approve_btn)

            view_btn = QPushButton("👁 View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            view_btn.clicked.connect(lambda checked, s=student: self.view_student(s))
            action_layout.addWidget(view_btn)

            self.students_table.setCellWidget(row, 7, action_widget)

    def load_requests(self):
        pending = [s for s in SchoolData.students if s['status'] == 'Pending']
        self.requests_table.setRowCount(len(pending))

        for row, student in enumerate(pending):
            self.requests_table.setItem(row, 0, QTableWidgetItem(student['lrn']))
            name = f"{student['first_name']} {student['last_name']}"
            self.requests_table.setItem(row, 1, QTableWidgetItem(name))
            self.requests_table.setItem(row, 2, QTableWidgetItem(student['grade_level']))
            self.requests_table.setItem(row, 3, QTableWidgetItem(student['strand']))
            self.requests_table.setItem(row, 4, QTableWidgetItem("2024-01-15"))
            self.requests_table.setItem(row, 5, QTableWidgetItem("Pending"))

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)

            approve_btn = QPushButton("✓ Approve")
            approve_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
            """)
            approve_btn.clicked.connect(lambda checked, lrn=student['lrn']: self.approve_student(lrn))

            reject_btn = QPushButton("✗ Reject")
            reject_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
            """)
            reject_btn.clicked.connect(lambda checked, lrn=student['lrn']: self.reject_student(lrn))

            action_layout.addWidget(approve_btn)
            action_layout.addWidget(reject_btn)
            self.requests_table.setCellWidget(row, 6, action_widget)

    def filter_students(self):
        search_text = self.search_input.text().lower()
        strand = self.strand_filter.currentText()

        filtered = []
        for student in self.all_students:
            name = f"{student['first_name']} {student['last_name']}".lower()
            lrn = student['lrn'].lower()

            matches_search = not search_text or search_text in name or search_text in lrn
            matches_strand = strand == "All" or student['strand'] == strand

            if matches_search and matches_strand:
                filtered.append(student)

        self.display_students(filtered)

    def approve_student(self, lrn):
        SchoolData.update_student_status(lrn, 'Enrolled')
        QMessageBox.information(self, "Success", f"Student with LRN {lrn} has been enrolled.")
        self.load_students()

    def reject_student(self, lrn):
        SchoolData.update_student_status(lrn, 'Rejected')
        QMessageBox.information(self, "Success", f"Student with LRN {lrn} has been rejected.")
        self.load_students()

    def view_student(self, student):
        info = f"""
        Student Information:

        Name: {student['first_name']} {student['middle_name']} {student['last_name']}
        LRN: {student['lrn']}
        Birth Date: {student['birth_date']}
        Gender: {student['gender']}

        Contact:
        Email: {student['email']}
        Phone: {student['phone']}

        Guardian: {student['guardian_first']} {student['guardian_last']}
        Guardian Phone: {student['guardian_phone']}
        Relationship: {student['relation']}

        Academic:
        Grade Level: {student['grade_level']}
        Strand: {student['strand']}
        Semester: {student['semester']}
        School Year: {student['school_year']}
        Status: {student['status']}
        """

        QMessageBox.information(self, "Student Details", info)

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.stack.setCurrentIndex(0)


# ========================================================================
# ADMIN LOGIN PAGE
# ========================================================================

class AdminLoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_box = QFrame()
        login_box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 40px;
                max-width: 400px;
            }
        """)
        login_layout = QVBoxLayout(login_box)

        # Back button
        back_btn = QPushButton("← Back to Portal Selection")
        back_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #e74c3c;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        # Title
        title = QLabel("👑 Admin Login")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #e74c3c; margin: 20px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter admin username")
        self.username_input.setStyleSheet(Styles.INPUT)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(Styles.INPUT)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(Styles.BUTTON_DANGER)
        login_btn.clicked.connect(self.login)

        # Demo credentials
        demo_box = QFrame()
        demo_box.setStyleSheet("background-color: #f8f9fa; border-radius: 5px; padding: 10px; margin-top: 20px;")
        demo_layout = QVBoxLayout(demo_box)
        demo_layout.addWidget(QLabel("Demo Credentials:"))
        demo_layout.addWidget(QLabel("Username: admin"))
        demo_layout.addWidget(QLabel("Password: admin123"))

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_btn)
        form_layout.addWidget(demo_box)

        login_layout.addWidget(back_btn)
        login_layout.addWidget(title)
        login_layout.addLayout(form_layout)

        main_layout.addWidget(login_box)
        self.setLayout(main_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter username and password")
            return

        user = SchoolData.authenticate(username, password)

        if user and user['role'] == 'admin':
            self.username_input.clear()
            self.password_input.clear()
            self.stack.parent().current_user = user
            self.stack.setCurrentIndex(8)  # Go to admin dashboard
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")


# ========================================================================
# ADMIN DASHBOARD
# ========================================================================

class AdminDashboard(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #e74c3c; color: white; padding: 15px;")
        header_layout = QHBoxLayout(header)

        title = QLabel("Admin Dashboard - System Administration")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.user_label = QLabel("Welcome, Admin")
        self.user_label.setStyleSheet("font-size: 14px;")

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        logout_btn.clicked.connect(self.logout)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.user_label)
        header_layout.addWidget(logout_btn)

        # Content tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #f5f6fa;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 10px 20px;
                background-color: #ecf0f1;
                border: none;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #e74c3c;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #c0392b;
                color: white;
            }
        """)

        # Users Management Tab
        self.users_tab = self.create_users_tab()

        # System Settings Tab
        self.settings_tab = self.create_settings_tab()

        # Audit Log Tab
        self.audit_tab = self.create_audit_tab()

        self.tabs.addTab(self.users_tab, "👥 User Management")
        self.tabs.addTab(self.settings_tab, "⚙️ System Settings")
        self.tabs.addTab(self.audit_tab, "📋 Audit Log")

        main_layout.addWidget(header)
        main_layout.addWidget(self.tabs, 1)

        self.setLayout(main_layout)
        self.load_users()

    def create_users_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Add user button
        add_user_btn = QPushButton("➕ Add New User")
        add_user_btn.setStyleSheet(Styles.BUTTON_SUCCESS)
        add_user_btn.clicked.connect(self.add_user)

        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels([
            "Username", "Role", "Name", "Status", "Actions"
        ])
        self.users_table.setStyleSheet(Styles.TABLE)
        self.users_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(add_user_btn)
        layout.addWidget(self.users_table)

        return tab

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # School Information
        school_group = QGroupBox("School Information")
        school_group.setStyleSheet(Styles.GROUPBOX)
        school_layout = QGridLayout(school_group)

        school_layout.addWidget(QLabel("School Name:"), 0, 0)
        self.school_name = QLineEdit("Springfield Academy")
        self.school_name.setStyleSheet(Styles.INPUT)
        school_layout.addWidget(self.school_name, 0, 1)

        school_layout.addWidget(QLabel("School Year:"), 1, 0)
        self.school_year = QLineEdit("2024-2025")
        self.school_year.setStyleSheet(Styles.INPUT)
        school_layout.addWidget(self.school_year, 1, 1)

        school_layout.addWidget(QLabel("Semester:"), 2, 0)
        self.semester = QComboBox()
        self.semester.addItems(["1st Semester", "2nd Semester"])
        self.semester.setStyleSheet(Styles.INPUT)
        school_layout.addWidget(self.semester, 2, 1)

        # Enrollment Settings
        enrollment_group = QGroupBox("Enrollment Settings")
        enrollment_group.setStyleSheet(Styles.GROUPBOX)
        enrollment_layout = QGridLayout(enrollment_group)

        enrollment_layout.addWidget(QLabel("Max Students per Strand:"), 0, 0)
        self.max_students = QSpinBox()
        self.max_students.setRange(10, 100)
        self.max_students.setValue(50)
        self.max_students.setStyleSheet(Styles.INPUT)
        enrollment_layout.addWidget(self.max_students, 0, 1)

        enrollment_layout.addWidget(QLabel("Enrollment Deadline:"), 1, 0)
        self.deadline = QDateEdit()
        self.deadline.setDate(QDate.currentDate().addMonths(1))
        self.deadline.setCalendarPopup(True)
        self.deadline.setStyleSheet(Styles.INPUT)
        enrollment_layout.addWidget(self.deadline, 1, 1)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet(Styles.BUTTON_PRIMARY)
        save_btn.clicked.connect(self.save_settings)

        layout.addWidget(school_group)
        layout.addWidget(enrollment_group)
        layout.addWidget(save_btn)
        layout.addStretch()

        return tab

    def create_audit_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Audit log table
        self.audit_table = QTableWidget()
        self.audit_table.setColumnCount(4)
        self.audit_table.setHorizontalHeaderLabels([
            "Timestamp", "User", "Action", "Details"
        ])
        self.audit_table.setStyleSheet(Styles.TABLE)

        # Sample audit data
        self.audit_table.setRowCount(5)
        audit_data = [
            ("2024-01-15 09:30", "admin", "User Login", "Admin logged in"),
            ("2024-01-15 10:15", "staff", "Student Approved", "LRN: 123456789012"),
            ("2024-01-15 11:00", "admin", "Settings Changed", "School year updated"),
            ("2024-01-14 15:30", "staff", "Student Added", "New enrollment"),
            ("2024-01-14 14:20", "admin", "User Created", "New staff account"),
        ]

        for i, (timestamp, user, action, details) in enumerate(audit_data):
            self.audit_table.setItem(i, 0, QTableWidgetItem(timestamp))
            self.audit_table.setItem(i, 1, QTableWidgetItem(user))
            self.audit_table.setItem(i, 2, QTableWidgetItem(action))
            self.audit_table.setItem(i, 3, QTableWidgetItem(details))

        layout.addWidget(self.audit_table)

        return tab

    def load_users(self):
        self.users_table.setRowCount(len(SchoolData.users))

        for row, user in enumerate(SchoolData.users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user['username']))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['role'].title()))

            name = user.get('name', '')
            if user['role'] == 'student' and 'student_lrn' in user:
                student = SchoolData.get_student_by_lrn(user['student_lrn'])
                if student:
                    name = f"{student['first_name']} {student['last_name']}"
            self.users_table.setItem(row, 2, QTableWidgetItem(name))

            self.users_table.setItem(row, 3, QTableWidgetItem("Active"))

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)

            edit_btn = QPushButton("✏️ Edit")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
            """)

            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
            """)

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            self.users_table.setCellWidget(row, 4, action_widget)

    def add_user(self):
        # Simple dialog to add user
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Add User")
        dialog.setText("This would open a form to add a new user.\nFor demo purposes, we'll keep it simple.")
        dialog.exec()

    def save_settings(self):
        QMessageBox.information(self, "Settings Saved", "System settings have been updated successfully.")

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.stack.setCurrentIndex(0)


# ========================================================================
# MAIN WINDOW
# ========================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Springfield Academy - SHS Enrollment System")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet(Styles.MAIN_WINDOW)

        # Store current user
        self.current_user = None

        # Stack widget for navigation
        self.stack = QStackedWidget()

        # Create pages
        self.login_page = LoginPage(self.stack)
        self.student_login = StudentLoginPage(self.stack)
        self.student_dashboard = StudentDashboard(self.stack)
        self.student_registration = StudentRegistrationPage(self.stack)
        self.staff_login = StaffLoginPage(self.stack)
        self.staff_dashboard = StaffDashboard(self.stack)
        self.admin_login = AdminLoginPage(self.stack)
        self.admin_dashboard = AdminDashboard(self.stack)

        # Add pages to stack
        self.stack.addWidget(self.login_page)  # index 0
        self.stack.addWidget(self.student_login)  # index 1
        self.stack.addWidget(self.student_dashboard)  # index 2
        self.stack.addWidget(self.student_registration)  # index 3
        self.stack.addWidget(self.staff_login)  # index 4
        self.stack.addWidget(self.staff_dashboard)  # index 5
        self.stack.addWidget(self.admin_login)  # index 6
        self.stack.addWidget(self.admin_dashboard)  # index 7

        self.setCentralWidget(self.stack)


# ========================================================================
# RUN APPLICATION
# ========================================================================

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())