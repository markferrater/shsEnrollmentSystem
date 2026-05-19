import sys
import json
import os
from datetime import date

from PyQt6.QtCore import Qt, QUrl, QTimer, QDate
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QStackedWidget, QGroupBox, QMessageBox, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QFileDialog,
    QDateEdit, QTextEdit
)

from FInal_Project.Controller.control import Students, Announcement
from FInal_Project.Controller.Login import login


# ══════════════════════════════════════════════════════════════════
#  LOGIN PAGE  (portal selector)
# ══════════════════════════════════════════════════════════════════
class LoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        box = QWidget()
        box_layout = QHBoxLayout(box)
        box.setFixedSize(750, 450)
        box.setStyleSheet("""
        QWidget { background: white; border-radius: 10px; padding: 20px; }
        #student_portal_box, #admin_box, #staff_box {
            background: gray; border-radius: 10px; padding: 20px;
        }
        #student_portal_box:hover, #admin_box:hover, #staff_box:hover {
            border: 4px solid blue;
        }
        #btn, #btn2, #btn3 { border: 1px solid gray; background: black; color: white; }
        #btn:hover, #btn2:hover, #btn3:hover { background: #c9c9c9; color: black; }
        #btn:pressed, #btn2:pressed, #btn3:pressed { background: black; color: white; }
        """)

        student_portal_box = QWidget()
        student_portal_box_layout = QVBoxLayout(student_portal_box)
        student_portal_box.setObjectName('student_portal_box')
        label = QLabel('Student Portal')

        label.setStyleSheet("""
             font-family: 'Inter';
             font-size: 18px;

        """)

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn = QPushButton('login')
        btn.clicked.connect(self.go_to_student)
        btn.setObjectName('btn')
        student_portal_box_layout.addWidget(label)
        student_portal_box_layout.addWidget(btn)

        staff_box = QWidget()
        staff_box_layout = QVBoxLayout(staff_box)
        staff_box.setObjectName('staff_box')
        label2 = QLabel('Staff Portal')

        label2.setStyleSheet("""
                    font-family: 'Inter';
                    font-size: 18px;

               """)

        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn2 = QPushButton('login')
        btn2.clicked.connect(self.go_to_staff)
        btn2.setObjectName('btn2')
        staff_box_layout.addWidget(label2)
        staff_box_layout.addWidget(btn2)

        admin_box = QWidget()
        admin_box_layout = QVBoxLayout(admin_box)
        admin_box.setObjectName('admin_box')
        label3 = QLabel('Admin Portal')

        label3.setStyleSheet("""
                    font-family: 'Inter';
                    font-size: 18px;

               """)

        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn3 = QPushButton('login')
        btn3.clicked.connect(self.go_to_admin)
        btn3.setObjectName('btn3')
        admin_box_layout.addWidget(label3)
        admin_box_layout.addWidget(btn3)

        box_layout.addWidget(student_portal_box)
        box_layout.addWidget(staff_box)
        box_layout.addWidget(admin_box)
        main_layout.addWidget(box)
        self.setLayout(main_layout)

    def go_to_student(self): self.stack.setCurrentIndex(1)

    def go_to_staff(self):   self.stack.setCurrentIndex(4)

    def go_to_admin(self):   self.stack.setCurrentIndex(5)


# ══════════════════════════════════════════════════════════════════
#  STUDENT PORTAL LOGIN
# ══════════════════════════════════════════════════════════════════
class studentPortal(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        box = QWidget()
        box_layout = QVBoxLayout(box)
        box.setFixedSize(450, 550)
        box.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")

        back_btn = QPushButton('<-back')
        back_btn.clicked.connect(self.back)
        back_btn.setStyleSheet("padding: 0px;")

        logo = QLabel()
        pixmap = QPixmap("Logo.png")
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        logo.setFixedSize(150, 150)

        title = QWidget()
        title.setFixedHeight(90)
        title.setStyleSheet("padding: 1px; background: black; color: white;")
        title_layout = QVBoxLayout(title)
        title_header = QLabel("Student Portal")
        title_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_paragraph = QLabel("Login to access your account")
        title_paragraph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_header)
        title_layout.addWidget(title_paragraph)

        form_box = QWidget()
        form_box.setObjectName('form_box')
        form_box.setStyleSheet("""
        #form_box { background: white; border: 1px solid gray; padding: 0px; }
        #user_name, #user_pass { padding: 0px; }
        #user_name_input, #user_pass_input {
            border: 1px solid gray; margin-top: 10px; padding: 0px; border-radius: 4px;
        }
        #login_btn { border-radius: 4px; background: black; color: white; }
        #login_btn:hover { background: gray; color: white; border-radius: 8px; }
        #login_btn:pressed { background: black; color: white; }
        """)
        form_box_layout = QVBoxLayout(form_box)

        user_name = QGroupBox("Username: ")
        user_name.setObjectName('user_name')
        user_name.setFixedHeight(50)
        user_name_layout = QHBoxLayout(user_name)
        self.user_name_input = QLineEdit()
        self.user_name_input.setObjectName('user_name_input')
        user_name_layout.addWidget(self.user_name_input)

        user_pass = QGroupBox("Password: ")
        user_pass.setFixedHeight(50)
        user_pass.setObjectName('user_pass')
        user_pass_layout = QHBoxLayout(user_pass)
        self.user_pass_input = QLineEdit()
        self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.user_pass_input.setObjectName('user_pass_input')
        user_pass_layout.addWidget(self.user_pass_input)

        self.user_pass_btn = QPushButton('Show pass')
        self.user_pass_btn.clicked.connect(self.toggle_pass)
        self.user_pass_btn.setStyleSheet("""
        padding: 0px; padding-left: 10px; border-radius: 5px;
        margin-left: 10px; margin-right: 300px;
        background: gray; color: white;
        """)

        login_btn = QPushButton('Log-in')
        login_btn.clicked.connect(lambda: self.go_to_student_portal(self.user_name_input, self.user_pass_input))
        login_btn.setObjectName('login_btn')

        register = QPushButton('New Student? Register here to enroll')
        register.clicked.connect(self.go_to_student_form)
        register.setObjectName('register')
        register.setStyleSheet("#register:hover { color: gray } #register:pressed { color: black }")

        form_box_layout.addWidget(user_name)
        form_box_layout.addWidget(user_pass)
        form_box_layout.addWidget(self.user_pass_btn)
        form_box_layout.addWidget(login_btn)
        form_box_layout.addWidget(register)

        box_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        box_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        box_layout.addWidget(title, 3)
        box_layout.addWidget(form_box)

        main_layout.addWidget(box)
        self.setLayout(main_layout)

    def toggle_pass(self):
        if self.user_pass_input.echoMode() == QLineEdit.EchoMode.Password:
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.user_pass_btn.setText("Hide pass ")
        else:
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.user_pass_btn.setText("Show pass")

    def check_pass(self, name, password):
        if name == '' or password == '':
            return 'empty'
        log = login(name, password)
        return log.check_pass_student()

    def back(self):
        self.stack.setCurrentIndex(0)

    def go_to_student_form(self):
        self.stack.setCurrentIndex(3)

    def go_to_student_portal(self, name, password):
        user = name.text()
        pas = password.text()
        result = self.check_pass(user, pas)

        if result == 'approved':
            lrn = Students.get_lrn_by_username(user)
            if lrn:
                student_data = Students.get_student_by_lrn(lrn)
                if student_data:
                    portal: StudentPortalAccount = self.stack.widget(2)
                    portal.load_student(student_data)
            self.user_pass_input.clear()
            self.user_name_input.clear()
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.stack.setCurrentIndex(2)
        elif result == 'empty':
            QMessageBox.warning(self, "Login Failed", "Please enter your credentials!")
        elif result == 'pending':
            QMessageBox.warning(self, "Account Pending",
                                "Your account is still pending approval.\nPlease wait for admin confirmation.")
        elif result == 'declined':
            QMessageBox.critical(self, "Account Declined",
                                 "Your enrollment has been declined.\nPlease contact the school.")
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password!")


# ══════════════════════════════════════════════════════════════════
#  STUDENT ENROLLMENT FORM
# ══════════════════════════════════════════════════════════════════
class StudentFormChild(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container.setStyleSheet('''
                background: #faf7ff;
                ''')

        container_layout = QVBoxLayout(container)
        container_layout.addStretch()

        student_form = QGroupBox()
        student_form.setStyleSheet('''
        background: #faf7ff;
        ''')
        student_form_layout = QVBoxLayout(student_form)

        # ── Personal Information ──
        personal_info_gbox = QGroupBox('Personal Information')
        personal_info_gbox_layout = QVBoxLayout(personal_info_gbox)
        personal_info_gbox_first_layout = QHBoxLayout()
        personal_info_gbox_second_layout = QHBoxLayout()
        personal_info_gbox_layout.addLayout(personal_info_gbox_first_layout)
        personal_info_gbox_layout.addLayout(personal_info_gbox_second_layout)

        personal_info_lrn = QGroupBox('LRN')
        personal_info_lrn_layout = QVBoxLayout(personal_info_lrn)
        personal_info_first_name = QGroupBox('First name')
        personal_info_first_name_layout = QVBoxLayout(personal_info_first_name)
        personal_info_middle_name = QGroupBox('Middle name')
        personal_info_middle_name_layout = QVBoxLayout(personal_info_middle_name)
        personal_info_last_name = QGroupBox('Last name')
        personal_info_last_name_layout = QVBoxLayout(personal_info_last_name)
        personal_info_date_of_birth = QGroupBox('Date of birth')
        personal_info_date_of_birth_layout = QVBoxLayout(personal_info_date_of_birth)
        personal_info_gender = QGroupBox('Gender')
        personal_info_gender_layout = QVBoxLayout(personal_info_gender)

        personal_info_lrn_input = QLineEdit()
        personal_info_first_name_input = QLineEdit()
        personal_info_middle_name_input = QLineEdit()
        personal_info_last_name_input = QLineEdit()
        personal_info_date_of_birth_input = QDateEdit()
        personal_info_date_of_birth_input.setCalendarPopup(True)
        personal_info_date_of_birth_input.setDate(QDate.currentDate())

        personal_info_gender_input = QComboBox()
        personal_info_gender_input.setPlaceholderText('Enter your Gender')
        personal_info_gender_input.addItems(["Male", "Female"])

        personal_info_lrn_layout.addWidget(personal_info_lrn_input)
        personal_info_first_name_layout.addWidget(personal_info_first_name_input)
        personal_info_middle_name_layout.addWidget(personal_info_middle_name_input)
        personal_info_last_name_layout.addWidget(personal_info_last_name_input)
        personal_info_date_of_birth_layout.addWidget(personal_info_date_of_birth_input)
        personal_info_gender_layout.addWidget(personal_info_gender_input)

        personal_info_gbox_first_layout.addWidget(personal_info_lrn)
        personal_info_gbox_first_layout.addWidget(personal_info_first_name)
        personal_info_gbox_first_layout.addWidget(personal_info_middle_name)
        personal_info_gbox_first_layout.addWidget(personal_info_last_name)
        personal_info_gbox_second_layout.addWidget(personal_info_date_of_birth)
        personal_info_gbox_second_layout.addWidget(personal_info_gender)

        # ── Contact Information ──
        contact_info_gbox = QGroupBox('Contact Information')
        contact_info_gbox_layout = QVBoxLayout(contact_info_gbox)
        contact_info_gbox_first_layout = QHBoxLayout()
        contact_info_gbox_layout.addLayout(contact_info_gbox_first_layout)

        contact_info_email = QGroupBox('Email address')
        contact_info_email_layout = QVBoxLayout(contact_info_email)
        contact_info_phone = QGroupBox('Phone number')
        contact_info_phone_layout = QVBoxLayout(contact_info_phone)

        contact_info_email_input = QLineEdit()
        contact_info_phone_input = QLineEdit()
        contact_info_phone_input.setMaxLength(10)

        contact_info_email_layout.addWidget(contact_info_email_input)
        contact_info_phone_layout.addWidget(contact_info_phone_input)
        contact_info_gbox_first_layout.addWidget(contact_info_email)
        contact_info_gbox_first_layout.addWidget(contact_info_phone)

        # ── Guardian Information ──
        guardian_info_gbox = QGroupBox('Guardian Information')
        guardian_info_gbox_layout = QVBoxLayout(guardian_info_gbox)
        guardian_info_gbox_first_layout = QHBoxLayout()
        guardian_info_gbox_second_layout = QHBoxLayout()
        guardian_info_gbox_layout.addLayout(guardian_info_gbox_first_layout)
        guardian_info_gbox_layout.addLayout(guardian_info_gbox_second_layout)

        guardian_info_first_name = QGroupBox('First name')
        guardian_info_first_name_layout = QVBoxLayout(guardian_info_first_name)
        guardian_info_middle_name = QGroupBox('Middle name')
        guardian_info_middle_name_layout = QVBoxLayout(guardian_info_middle_name)
        guardian_info_last_name = QGroupBox('Last name')
        guardian_info_last_name_layout = QVBoxLayout(guardian_info_last_name)
        guardian_info_phone_number = QGroupBox('Guardian Phone Number')
        guardian_info_phone_number_layout = QVBoxLayout(guardian_info_phone_number)
        guardian_info_current_rel = QGroupBox('Current Relationship')
        guardian_info_current_rel_layout = QVBoxLayout(guardian_info_current_rel)

        guardian_info_first_name_input = QLineEdit()
        guardian_info_middle_name_input = QLineEdit()
        guardian_info_last_name_input = QLineEdit()
        guardian_info_phone_number_input = QLineEdit()
        guardian_info_current_rel_input = QLineEdit()

        guardian_info_first_name_layout.addWidget(guardian_info_first_name_input)
        guardian_info_middle_name_layout.addWidget(guardian_info_middle_name_input)
        guardian_info_last_name_layout.addWidget(guardian_info_last_name_input)
        guardian_info_phone_number_layout.addWidget(guardian_info_phone_number_input)
        guardian_info_current_rel_layout.addWidget(guardian_info_current_rel_input)

        guardian_info_gbox_first_layout.addWidget(guardian_info_first_name)
        guardian_info_gbox_first_layout.addWidget(guardian_info_middle_name)
        guardian_info_gbox_first_layout.addWidget(guardian_info_last_name)
        guardian_info_gbox_second_layout.addWidget(guardian_info_phone_number)
        guardian_info_gbox_second_layout.addWidget(guardian_info_current_rel)

        # ── Academic Information ──
        academic_info_gbox = QGroupBox('Academic Information')
        academic_info_gbox_layout = QVBoxLayout(academic_info_gbox)
        academic_info_first_layout = QHBoxLayout()
        academic_info_gbox_layout.addLayout(academic_info_first_layout)

        academic_info_grade_level = QGroupBox('Grade level')
        academic_info_grade_level_layout = QHBoxLayout(academic_info_grade_level)
        academic_info_strand = QGroupBox('Strand')
        academic_info_strand_layout = QHBoxLayout(academic_info_strand)
        academic_info_semester = QGroupBox('Semester')
        academic_info_semester_layout = QHBoxLayout(academic_info_semester)
        academic_info_previous_school = QGroupBox('Previous school')
        academic_info_previous_school_layout = QHBoxLayout(academic_info_previous_school)

        academic_info_grade_level_input = QLineEdit()
        academic_info_strand_input = QComboBox()
        academic_info_strand_input.setPlaceholderText('Select Strand')
        academic_info_strand_input.addItems(['STEM', 'ABM', 'GAS', 'HUMMS', 'TVL'])
        academic_info_semester_input = QLineEdit()
        academic_info_previous_school_input = QLineEdit()

        academic_info_grade_level_layout.addWidget(academic_info_grade_level_input)
        academic_info_strand_layout.addWidget(academic_info_strand_input)
        academic_info_semester_layout.addWidget(academic_info_semester_input)
        academic_info_previous_school_layout.addWidget(academic_info_previous_school_input)

        academic_info_first_layout.addWidget(academic_info_grade_level)
        academic_info_first_layout.addWidget(academic_info_strand)
        academic_info_first_layout.addWidget(academic_info_semester)
        academic_info_first_layout.addWidget(academic_info_previous_school)

        # ── Submit ──
        submit = QPushButton('Submit Enrollment')
        submit.setStyleSheet('''
        background: #5fb5d4;
        color: white;
        ''')

        submit.clicked.connect(lambda: self.submit_student_data(
            personal_info_lrn_input, personal_info_first_name_input,
            personal_info_middle_name_input, personal_info_last_name_input,
            personal_info_date_of_birth_input, personal_info_gender_input,
            contact_info_email_input, contact_info_phone_input,
            guardian_info_first_name_input, guardian_info_middle_name_input,
            guardian_info_last_name_input, guardian_info_phone_number_input,
            guardian_info_current_rel_input, academic_info_grade_level_input,
            academic_info_strand_input, academic_info_semester_input,
            academic_info_previous_school_input
        ))

        student_form_layout.addWidget(personal_info_gbox)
        student_form_layout.addWidget(contact_info_gbox)
        student_form_layout.addWidget(guardian_info_gbox)
        student_form_layout.addWidget(academic_info_gbox)
        student_form_layout.addWidget(submit)

        container_layout.addWidget(student_form)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def submit_student_data(self, *inputs):
        lrn = inputs[0].text().strip()
        fname = inputs[1].text().strip()
        lname = inputs[3].text().strip()

        if (not inputs[0].text() or  # LRN
                not inputs[1].text() or  # First Name
                not inputs[2].text() or  # Last Name
                not inputs[3].text() or  # Last Name
                not inputs[4].date().toString("MMM d yyyy") or  # Last Name
                not inputs[5].currentText() or  # Last Name
                not inputs[6].text() or  # Example required field
                not inputs[7].text() or
                not inputs[8].text() or
                not inputs[9].text() or
                not inputs[10].text() or
                not inputs[11].text() or
                not inputs[12].text() or
                not inputs[13].text() or
                not inputs[14].currentText() or
                not inputs[15].text() or
                not inputs[16].text()):
            QMessageBox.warning(self, "Incomplete Form", "Please fill out all the form.")
            return

        student = Students(
            inputs[0].text(), inputs[1].text(), inputs[2].text(), inputs[3].text(),
            inputs[4].date().toString("MMM d yyyy"), inputs[5].currentText(),
            inputs[6].text(), inputs[7].text(),
            inputs[8].text(), inputs[9].text(), inputs[10].text(), inputs[11].text(),
            inputs[12].text(), inputs[13].text(), inputs[14].currentText(),
            inputs[15].text(), inputs[16].text()
        )

        try:
            student.add_student()
            QMessageBox.information(self, "Success",
                                    f"Student registered!\n\nUsername: {inputs[6].text()}\n"
                                    f"Default Password: {inputs[0].text()}\n\nYour account is pending admin approval.")
            for inp in inputs:
                inp.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save student:\n{e}")


class StudentForm(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        content = QWidget()
        content.setStyleSheet("background: white;")
        content_layout = QVBoxLayout(content)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header.setStyleSheet("background: gray; color: white;")
        header1 = QLabel('Student Form')
        header1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header2 = QPushButton('Exit')
        header2.setStyleSheet('''
        background: red;
        color: white;
        ''')


        header2.clicked.connect(self.go_back)
        header_layout.addWidget(header1, 2)
        header_layout.addWidget(header2)
        content_layout.addWidget(header)

        row = StudentFormChild()
        content_layout.addWidget(row)
        main_layout.addWidget(content)

    def go_back(self): self.stack.setCurrentIndex(1)


# ══════════════════════════════════════════════════════════════════
#  STUDENT PORTAL ACCOUNT
# ══════════════════════════════════════════════════════════════════
class StudentPortalAccount(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self._current_student = {}

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(90)
        header.setStyleSheet('background-color: #d0d0d0;')
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)

        logo = QLabel()
        pixmap = QPixmap('Logo.png')
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        logo.setFixedSize(80, 80)

        center_widget = QWidget()
        center_widget.setStyleSheet('background: transparent;')
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(4)

        self.welcome_label = QLabel('Welcome, Student')
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet(
            "color: #1a1a2e; font-size: 18px; font-weight: bold; background: transparent;")

        nav_row = QWidget()
        nav_row.setStyleSheet('background: transparent;')
        nav_row_layout = QHBoxLayout(nav_row)
        nav_row_layout.setContentsMargins(0, 0, 0, 0)
        nav_row_layout.setSpacing(8)
        nav_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        nav_style = """
            QPushButton { background: #b0b0b0; color: #1a1a2e; border-radius: 4px;
                          padding: 5px 16px; font-size: 12px; font-weight: 500; }
            QPushButton:hover  { background: #4f46e5; color: white; }
            QPushButton:pressed { background: #3730a3; color: white; }
        """
        btn_dashboard = QPushButton('Dashboard')
        btn_profile = QPushButton('My Profile')
        btn_schedule = QPushButton('View Schedules')
        btn_grades = QPushButton('View Grades')
        for b in [btn_dashboard, btn_profile, btn_schedule, btn_grades]:
            b.setStyleSheet(nav_style)
            nav_row_layout.addWidget(b)

        center_layout.addWidget(self.welcome_label)
        center_layout.addWidget(nav_row)

        logout_btn = QPushButton('Logout')
        logout_btn.setFixedSize(80, 30)
        logout_btn.clicked.connect(self.go_to_login)
        logout_btn.setStyleSheet("""
            QPushButton { background: white; color: black; border: 1px solid gray;
                          border-radius: 4px; font-size: 12px; }
            QPushButton:hover { background: #ef4444; color: white; border: none; }
        """)

        header_layout.addWidget(logo)
        header_layout.addWidget(center_widget, 1)
        header_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignTop)

        body = QWidget()
        body.setStyleSheet('background-color: #dbeafe;')
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(40, 30, 40, 30)
        body_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.inner_stack = QStackedWidget()
        self.inner_stack.setMaximumWidth(700)
        self.inner_stack.setStyleSheet('background: transparent;')

        # Pages built lazily — populated in load_student()
        self._dashboard_page = self._make_dashboard()
        self._profile_page = self._make_profile()
        self._schedule_page = self._make_schedule_placeholder()
        self._grades_page = self._make_grades_placeholder()

        self.inner_stack.addWidget(self._dashboard_page)  # 0
        self.inner_stack.addWidget(self._profile_page)  # 1
        self.inner_stack.addWidget(self._schedule_page)  # 2
        self.inner_stack.addWidget(self._grades_page)  # 3

        btn_dashboard.clicked.connect(lambda: self.inner_stack.setCurrentIndex(0))
        btn_profile.clicked.connect(lambda: self.inner_stack.setCurrentIndex(1))
        btn_schedule.clicked.connect(lambda: self.inner_stack.setCurrentIndex(2))
        btn_grades.clicked.connect(lambda: self.inner_stack.setCurrentIndex(3))

        body_layout.addWidget(self.inner_stack)
        main_layout.addWidget(header)
        main_layout.addWidget(body, 1)

    # ── Load student data after login ────────────────────────────────
    def load_student(self, data: dict):
        self._current_student = data
        name = f"{data.get('First_name', '')} {data.get('Last_name', '')}"
        self.welcome_label.setText(f"Welcome, {name}")
        self._refresh_profile(data)
        self._refresh_dashboard()
        self._refresh_schedule(data)
        self._refresh_grades(data)

    # ── Dashboard — announcements from DB ────────────────────────────
    def _make_dashboard(self):
        page = QWidget()
        page.setStyleSheet('background: transparent;')
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        ann_box = QGroupBox('Announcements')
        ann_box.setStyleSheet("""
            QGroupBox { background-color: #c8c8c8; border-radius: 8px;
                        font-size: 14px; font-weight: bold; padding: 10px; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;
                               padding: 0 8px; color: #1a1a2e; }
        """)
        ann_layout = QVBoxLayout(ann_box)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)
        scroll.setStyleSheet("background: white; border-radius: 6px;")

        self._ann_container = QWidget()
        self._ann_container.setStyleSheet("background: white;")
        self._ann_inner_layout = QVBoxLayout(self._ann_container)
        self._ann_inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._ann_inner_layout.setContentsMargins(10, 10, 10, 10)

        scroll.setWidget(self._ann_container)
        ann_layout.addWidget(scroll)
        layout.addWidget(ann_box)
        layout.addStretch()
        return page

    def _refresh_dashboard(self):
        # Clear old widgets
        while self._ann_inner_layout.count():
            child = self._ann_inner_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        announcements = Announcement.get_for_target('Student')
        if not announcements:
            lbl = QLabel('No announcements at this time.')
            lbl.setStyleSheet('color: #6b7280; font-size: 12px; background: transparent;')
            self._ann_inner_layout.addWidget(lbl)
            return

        for ann in announcements:
            card = QWidget()
            card.setStyleSheet("""
                background: #f0f4ff; border-radius: 6px; margin-bottom: 6px;
                border-left: 4px solid #4f46e5;
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 10, 8)

            title_lbl = QLabel(ann.get('title', ''))
            title_lbl.setStyleSheet(
                'color: #1a1a2e; font-size: 13px; font-weight: bold; background: transparent;')

            date_str = str(ann.get('posted_date', ''))[:16]
            meta_lbl = QLabel(f"Posted: {date_str}  |  To: {ann.get('target', '')}")
            meta_lbl.setStyleSheet('color: #6b7280; font-size: 10px; background: transparent;')

            content_lbl = QLabel(ann.get('content', ''))
            content_lbl.setWordWrap(True)
            content_lbl.setStyleSheet('color: #374151; font-size: 11px; background: transparent;')

            card_layout.addWidget(title_lbl)
            card_layout.addWidget(meta_lbl)
            card_layout.addWidget(content_lbl)
            self._ann_inner_layout.addWidget(card)

    # ── Profile ───────────────────────────────────────────────────────
    def _make_profile(self):
        page = QWidget()
        page.setStyleSheet('background: transparent;')
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        profile_box = QGroupBox('My Profile')
        profile_box.setStyleSheet("""
            QGroupBox { background-color: #c8c8c8; border-radius: 8px;
                        font-size: 14px; font-weight: bold; padding: 10px; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;
                               padding: 0 8px; color: #1a1a2e; }
        """)
        profile_layout = QVBoxLayout(profile_box)

        self._profile_labels = {}
        for key in ['LRN', 'Name', 'Date of Birth', 'Gender', 'Email', 'Phone',
                    'Grade Level', 'Strand', 'Semester', 'Previous School']:
            row = QWidget()
            row.setStyleSheet('background: white; border-radius: 6px; margin-bottom: 4px;')
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 6, 8, 6)
            key_lbl = QLabel(key + ':')
            key_lbl.setFixedWidth(120)
            key_lbl.setStyleSheet(
                'color: #4f46e5; font-size: 11px; font-weight: bold; background: transparent;')
            val_lbl = QLabel('—')
            val_lbl.setStyleSheet('color: #1a1a2e; font-size: 12px; background: transparent;')
            self._profile_labels[key] = val_lbl
            row_layout.addWidget(key_lbl)
            row_layout.addWidget(val_lbl, 1)
            profile_layout.addWidget(row)

        layout.addWidget(profile_box)
        layout.addStretch()
        return page

    def _refresh_profile(self, data: dict):
        fields = {
            'LRN': data.get('student_lrn', ''),
            'Name': f"{data.get('First_name', '')} {data.get('Middle_name', '')} {data.get('Last_name', '')}",
            'Date of Birth': data.get('Date_of_birth', ''),
            'Gender': data.get('Gender', ''),
            'Email': data.get('Email_address', ''),
            'Phone': data.get('Phone_number', ''),
            'Grade Level': data.get('Grade_level', ''),
            'Strand': data.get('Strand', ''),
            'Semester': data.get('Semester', ''),
            'Previous School': data.get('Previous_school', ''),
        }
        for key, lbl in self._profile_labels.items():
            lbl.setText(str(fields.get(key, '') or '—'))

    # ── Schedule ──────────────────────────────────────────────────────
    def _make_schedule_placeholder(self):
        page = QWidget()
        page.setStyleSheet('background: transparent;')
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # ── GroupBox — identical style to My Profile ──
        self._sched_box = QGroupBox('Class Schedule')
        self._sched_box.setStyleSheet("""
            QGroupBox { background-color: #c8c8c8; border-radius: 8px;
                        font-size: 14px; font-weight: bold; padding: 10px; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;
                               padding: 0 8px; color: #1a1a2e; }
        """)
        sched_box_layout = QVBoxLayout(self._sched_box)
        sched_box_layout.setSpacing(6)
        sched_box_layout.setContentsMargins(6, 12, 6, 6)

        # ── Filter row: Grade Level combobox + Semester combobox ──
        filter_row = QWidget()
        filter_row.setStyleSheet('background: white; border-radius: 6px;')
        filter_layout = QHBoxLayout(filter_row)
        filter_layout.setContentsMargins(8, 6, 8, 6)
        filter_layout.setSpacing(12)

        grade_lbl = QLabel('Grade Level:')
        grade_lbl.setFixedWidth(90)
        grade_lbl.setStyleSheet(
            'color: #4f46e5; font-size: 11px; font-weight: bold; background: transparent;')

        self._sched_grade_combo = QComboBox()
        self._sched_grade_combo.addItems(['Grade 11', 'Grade 12'])
        self._sched_grade_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db; border-radius: 4px;
                padding: 3px 8px; font-size: 12px; color: #1a1a2e;
                background: white; min-width: 100px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background: white; color: #1a1a2e; }
        """)

        sem_lbl = QLabel('Semester:')
        sem_lbl.setFixedWidth(70)
        sem_lbl.setStyleSheet(
            'color: #4f46e5; font-size: 11px; font-weight: bold; background: transparent;')

        self._sched_sem_combo = QComboBox()
        self._sched_sem_combo.addItems(['1st Semester', '2nd Semester'])
        self._sched_sem_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db; border-radius: 4px;
                padding: 3px 8px; font-size: 12px; color: #1a1a2e;
                background: white; min-width: 110px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background: white; color: #1a1a2e; }
        """)

        # Connect both comboboxes to re-render subjects instantly on change
        self._sched_grade_combo.currentTextChanged.connect(self._on_sched_filter_changed)
        self._sched_sem_combo.currentTextChanged.connect(self._on_sched_filter_changed)

        filter_layout.addWidget(grade_lbl)
        filter_layout.addWidget(self._sched_grade_combo)
        filter_layout.addSpacing(8)
        filter_layout.addWidget(sem_lbl)
        filter_layout.addWidget(self._sched_sem_combo)
        filter_layout.addStretch()

        # ── Scrollable subject rows ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('QScrollArea { background: transparent; border: none; }')

        self._sched_scroll_widget = QWidget()
        self._sched_scroll_widget.setStyleSheet('background: transparent;')
        self._sched_inner_layout = QVBoxLayout(self._sched_scroll_widget)
        self._sched_inner_layout.setContentsMargins(0, 0, 0, 0)
        self._sched_inner_layout.setSpacing(4)
        self._sched_inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        loading = QLabel('Loading schedule…')
        loading.setStyleSheet('color: #6b7280; font-size: 12px; background: transparent;')
        self._sched_inner_layout.addWidget(loading)

        scroll.setWidget(self._sched_scroll_widget)

        sched_box_layout.addWidget(filter_row)
        sched_box_layout.addWidget(scroll)

        layout.addWidget(self._sched_box)
        layout.addStretch()
        return page

    def _on_sched_filter_changed(self):
        """Called when either combobox changes — re-renders the subject list."""
        self._render_subjects()

    def _refresh_schedule(self, data: dict):
        """Called once after login to set combobox defaults from student data, then render."""
        strand      = (data.get('Strand') or '').strip()
        grade_level = (data.get('Grade_level') or '').strip()

        # Pre-select the student's own grade level if it matches an option
        idx = self._sched_grade_combo.findText(grade_level)
        if idx >= 0:
            self._sched_grade_combo.blockSignals(True)
            self._sched_grade_combo.setCurrentIndex(idx)
            self._sched_grade_combo.blockSignals(False)

        # Update title with strand shown automatically
        self._sched_box.setTitle(f'Class Schedule  —  {strand}')

        # Render subjects for the pre-selected grade + default 1st Semester
        self._render_subjects()

    def _render_subjects(self):
        """Clears the list and redraws subjects for the currently selected grade + semester."""
        # Clear previous rows
        while self._sched_inner_layout.count():
            child = self._sched_inner_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        strand      = (self._current_student.get('Strand') or '').strip()
        grade_level = self._sched_grade_combo.currentText()
        semester    = self._sched_sem_combo.currentText()

        subjects = Students.get_subjects(strand, grade_level, semester)

        if not subjects:
            lbl = QLabel(f'No subjects found for {strand}  •  {grade_level}  •  {semester}.')
            lbl.setWordWrap(True)
            lbl.setStyleSheet(
                'color: #6b7280; font-size: 12px; background: transparent; padding: 10px;')
            self._sched_inner_layout.addWidget(lbl)
            return

        # ── Header row showing current filter summary — profile-key style ──
        summary_row = QWidget()
        summary_row.setStyleSheet('background: white; border-radius: 6px; margin-bottom: 2px;')
        summary_layout = QHBoxLayout(summary_row)
        summary_layout.setContentsMargins(8, 6, 8, 6)

        summary_key = QLabel('Showing:')
        summary_key.setFixedWidth(120)
        summary_key.setStyleSheet(
            'color: #4f46e5; font-size: 11px; font-weight: bold; background: transparent;')
        summary_val = QLabel(f'{grade_level}  •  {semester}  •  {len(subjects)} subject(s)')
        summary_val.setStyleSheet('color: #1a1a2e; font-size: 12px; background: transparent;')

        summary_layout.addWidget(summary_key)
        summary_layout.addWidget(summary_val, 1)
        self._sched_inner_layout.addWidget(summary_row)

        # ── One row per subject — identical layout to My Profile rows ──
        for s in subjects:
            row = QWidget()
            row.setStyleSheet('background: white; border-radius: 6px; margin-bottom: 4px;')
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 6, 8, 6)

            # Subject name — blue bold, same as profile key label
            name_lbl = QLabel(s.get('subject_name', ''))
            name_lbl.setFixedWidth(120)
            name_lbl.setWordWrap(True)
            name_lbl.setStyleSheet(
                'color: #4f46e5; font-size: 11px; font-weight: bold; background: transparent;')

            # Units — dark, same as profile value label
            units_lbl = QLabel(f"{s.get('units', '')} unit(s)")
            units_lbl.setStyleSheet(
                'color: #1a1a2e; font-size: 12px; background: transparent;')

            row_layout.addWidget(name_lbl)
            row_layout.addWidget(units_lbl, 1)
            self._sched_inner_layout.addWidget(row)



    # ── Grades — placeholder replaced by _refresh_grades ─────────────
    def _make_grades_placeholder(self):
        page = QWidget()
        page.setStyleSheet('background: transparent;')
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        self._grades_box = QGroupBox('My Grades')
        self._grades_box.setStyleSheet("""
            QGroupBox { background-color: #c8c8c8; border-radius: 8px;
                        font-size: 14px; font-weight: bold; padding: 10px; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center;
                               padding: 0 8px; color: #1a1a2e; }
        """)
        self._grades_layout = QVBoxLayout(self._grades_box)

        lbl = QLabel('Loading grades…')
        lbl.setStyleSheet('color: #6b7280; font-size: 12px; background: transparent;')
        self._grades_layout.addWidget(lbl)

        layout.addWidget(self._grades_box)
        layout.addStretch()
        return page

    def _refresh_grades(self, data: dict):
        # Clear existing rows
        while self._grades_layout.count():
            child = self._grades_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # This system is for enrollment only — no grades tracking
        lbl = QLabel('Grades are not available in this system.\nPlease contact your teacher for grade inquiries.')
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet('color: #6b7280; font-size: 12px; background: transparent; padding: 20px;')
        self._grades_layout.addWidget(lbl)

    def go_to_login(self):
        self._current_student = {}
        self.stack.setCurrentIndex(1)


# ══════════════════════════════════════════════════════════════════
#  STAFF PORTAL LOGIN
# ══════════════════════════════════════════════════════════════════
class staffPortal(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        box = QWidget()
        box_layout = QVBoxLayout(box)
        box.setFixedSize(450, 550)
        box.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")

        back_btn = QPushButton('<-back')
        back_btn.clicked.connect(self.back)
        back_btn.setStyleSheet("padding: 0px;")

        logo = QLabel()
        pixmap = QPixmap("Logo.png")
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        logo.setFixedSize(150, 150)

        title = QWidget()
        title.setFixedHeight(90)
        title.setStyleSheet("padding: 1px; background: black; color: white;")
        title_layout = QVBoxLayout(title)
        title_header = QLabel("Staff Portal")
        title_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_paragraph = QLabel("Registrar Login")
        title_paragraph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_header)
        title_layout.addWidget(title_paragraph)

        form_box = QWidget()
        form_box.setObjectName('form_box')
        form_box.setStyleSheet("""
        #form_box { background: white; border: 1px solid gray; padding: 0px; }
        #user_name, #user_pass { padding: 0px; }
        #user_name_input, #user_pass_input {
            border: 1px solid gray; margin-top: 10px; padding: 0px;
            border-radius: 4px; height: 50px; }
        #login_btn { border-radius: 4px; background: black; color: white; }
        #login_btn:hover  { background: gray; color: white; border-radius: 8px; }
        #login_btn:pressed { background: black; color: white; }
        """)
        form_box_layout = QVBoxLayout(form_box)

        user_name = QGroupBox("Username: ")
        user_name.setObjectName('user_name')
        user_name.setFixedHeight(50)
        user_name_layout = QHBoxLayout(user_name)
        self.user_name_input = QLineEdit()
        self.user_name_input.setObjectName('user_name_input')
        user_name_layout.addWidget(self.user_name_input)

        user_pass = QGroupBox("Password: ")
        user_pass.setFixedHeight(50)
        user_pass.setObjectName('user_pass')
        user_pass_layout = QHBoxLayout(user_pass)
        self.user_pass_input = QLineEdit()
        self.user_pass_input.setObjectName('user_pass_input')
        self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        user_pass_layout.addWidget(self.user_pass_input)

        self.user_pass_btn = QPushButton('Show pass')
        self.user_pass_btn.clicked.connect(self.toggle_pass)
        self.user_pass_btn.setStyleSheet("""
        padding: 0px; padding-left: 10px; border-radius: 5px;
        margin-left: 10px; margin-right: 300px;
        background: gray; color: white;
        """)

        login_btn = QPushButton('Log-in')
        login_btn.clicked.connect(
            lambda: self.go_to_staff_portal(self.user_name_input, self.user_pass_input))
        login_btn.setObjectName('login_btn')

        form_box_layout.addWidget(user_name)
        form_box_layout.addWidget(user_pass)
        form_box_layout.addWidget(self.user_pass_btn)
        form_box_layout.addWidget(login_btn)

        box_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        box_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        box_layout.addWidget(title)
        box_layout.addWidget(form_box, 2)
        main_layout.addWidget(box)
        self.setLayout(main_layout)

    def toggle_pass(self):
        if self.user_pass_input.echoMode() == QLineEdit.EchoMode.Password:
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.user_pass_btn.setText("Hide pass ")
        else:
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.user_pass_btn.setText("Show pass")

    def back(self):
        self.stack.setCurrentIndex(0)

    def go_to_staff_portal(self, name, password):
        user = name.text().strip()
        pas = password.text().strip()

        if not user or not pas:
            QMessageBox.warning(self, "Login Failed", "Please enter your credentials.")
            return

        log = login(user, pas)
        result = log.check_pass_staff()

        if result == 'approved':
            self.user_pass_input.clear()
            self.user_name_input.clear()
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            portal: StaffPortalAccount = self.stack.widget(6)
            portal.refresh_table()
            self.stack.setCurrentIndex(6)
        elif result in ('not_found', 'wrong_password'):
            QMessageBox.critical(self, "Login Failed", "These credentials do not match our records.")
        else:
            QMessageBox.critical(self, "Error", "An error occurred. Please try again.")


# ══════════════════════════════════════════════════════════════════
#  STAFF PORTAL ACCOUNT
#  Staff can: view/search/filter students, approve/decline, view details
#  Staff cannot: delete, generate reports, manage accounts
# ══════════════════════════════════════════════════════════════════
class StaffPortalAccount(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet('background: #1a1d2e;')
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)

        logo = QLabel()
        pix = QPixmap('Logo.png')
        logo.setPixmap(pix)
        logo.setScaledContents(True)
        logo.setFixedSize(50, 50)

        title_lbl = QLabel('Staff Portal — Enrollment Management')
        title_lbl.setStyleSheet(
            'color: white; font-size: 16px; font-weight: bold; background: transparent;')

        logout_btn = QPushButton('Logout')
        logout_btn.setFixedSize(80, 30)
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton { background: #ef4444; color: white; border-radius: 4px; font-size: 12px; }
            QPushButton:hover { background: #b91c1c; }
        """)

        header_layout.addWidget(logo)
        header_layout.addWidget(title_lbl, 1)
        header_layout.addWidget(logout_btn)

        toolbar = QWidget()
        toolbar.setFixedHeight(50)
        toolbar.setStyleSheet('background: #2d3561; padding: 4px;')
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(12, 4, 12, 4)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by name, LRN, or strand…')
        self.search_input.setFixedWidth(260)
        self.search_input.setStyleSheet("""
            border: 1px solid #6c7caa; border-radius: 4px;
            padding: 4px 8px; color: white; background: #1a1d2e;
        """)
        self.search_input.textChanged.connect(self._on_search)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['All', 'Pending', 'Approved', 'Declined'])
        self.filter_combo.setStyleSheet("""
            QComboBox { background: #1a1d2e; color: white; border: 1px solid #6c7caa;
                        border-radius: 4px; padding: 4px 8px; min-width: 100px; }
            QComboBox QAbstractItemView { background: #1a1d2e; color: white; }
        """)
        self.filter_combo.currentTextChanged.connect(self._on_filter)

        refresh_btn = QPushButton('⟳ Refresh')
        refresh_btn.setFixedWidth(90)
        refresh_btn.clicked.connect(self.refresh_table)
        refresh_btn.setStyleSheet("""
            QPushButton { background: #4f46e5; color: white; border-radius: 4px; padding: 4px 10px; }
            QPushButton:hover { background: #3730a3; }
        """)

        filter_lbl = QLabel('Filter:')
        filter_lbl.setStyleSheet('color: white;')
        toolbar_layout.addWidget(filter_lbl)
        toolbar_layout.addWidget(self.filter_combo)
        toolbar_layout.addSpacing(12)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ['LRN', 'First Name', 'Last Name', 'Grade', 'Strand', 'Semester', 'Email', 'Status'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget { background: white; gridline-color: #e5e7eb; }
            QHeaderView::section { background: #1a1d2e; color: white; padding: 6px; font-weight: bold; }
            QTableWidget::item:selected { background: #dbeafe; color: #1a1d2e; }
        """)

        action_bar = QWidget()
        action_bar.setFixedHeight(50)
        action_bar.setStyleSheet('background: #f3f4f6; border-top: 1px solid #e5e7eb;')
        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(12, 6, 12, 6)

        view_btn = QPushButton('👁 View Details')

        for btn in [view_btn]:
            btn.setFixedHeight(34)
            toolbar_layout.addWidget(btn)

        view_btn.setStyleSheet("""
            QPushButton { background: #4f46e5; color: white; border-radius: 4px; padding: 0 16px; }
            QPushButton:hover { background: #3730a3; }
        """)

        view_btn.clicked.connect(self._view_details)

        action_layout.addStretch()
        self.status_lbl = QLabel('')
        self.status_lbl.setStyleSheet('color: #6b7280; font-size: 11px;')
        action_layout.addWidget(self.status_lbl)

        main_layout.addWidget(header)
        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.table, 1)
        main_layout.addWidget(action_bar)

        self._all_rows: list[dict] = []

    def refresh_table(self):
        self._all_rows = Students.get_all_students()
        self._populate_table(self._all_rows)

    def _populate_table(self, rows: list[dict]):
        self.table.setRowCount(0)
        for row_data in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            cols = ['student_lrn', 'First_name', 'Last_name',
                    'Grade_level', 'Strand', 'Semester', 'Email_address', 'Status']
            for c, col in enumerate(cols):
                val = row_data.get(col, '') or ''
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 'Status':
                    color_map = {'Pending': '#fef3c7', 'Approved': '#d1fae5', 'Declined': '#fee2e2'}
                    item.setBackground(QColor(color_map.get(str(val), 'white')))
                self.table.setItem(r, c, item)
        self.status_lbl.setText(f'{len(rows)} record(s) shown')

    def _on_search(self, text):
        results = Students.search_students(text.strip()) if text.strip() else self._all_rows
        f = self.filter_combo.currentText()
        if f != 'All':
            results = [r for r in results if r.get('Status') == f]
        self._populate_table(results)

    def _on_filter(self, value):
        base = self._all_rows if value == 'All' else \
            [r for r in self._all_rows if r.get('Status') == value]
        kw = self.search_input.text().strip()
        if kw:
            base = [r for r in base if kw.lower() in str(r).lower()]
        self._populate_table(base)

    def _selected_lrn(self) -> str | None:
        row = self.table.currentRow()
        item = self.table.item(row, 0) if row >= 0 else None
        return item.text() if item else None

    def _change_status(self, new_status: str):
        lrn = self._selected_lrn()
        if not lrn:
            QMessageBox.warning(self, "No Selection", "Please select a student first.")
            return
        ok = Students.update_student_status(lrn, new_status)
        if ok:
            QMessageBox.information(self, "Updated", f"Student {lrn} status set to '{new_status}'.")
            self.refresh_table()
        else:
            QMessageBox.critical(self, "Error", "Failed to update status. Check your DB connection.")

    def _view_details(self):
        lrn = self._selected_lrn()
        if not lrn:
            QMessageBox.warning(self, "No Selection", "Please select a student first.")
            return
        data = Students.get_student_by_lrn(lrn)
        if not data:
            QMessageBox.warning(self, "Not Found", "Could not retrieve student data.")
            return
        msg = "\n".join([
            f"LRN:           {data.get('student_lrn', '')}",
            f"Name:          {data.get('First_name', '')} {data.get('Middle_name', '')} {data.get('Last_name', '')}",
            f"Date of Birth: {data.get('Date_of_birth', '')}",
            f"Gender:        {data.get('Gender', '')}",
            f"Email:         {data.get('Email_address', '')}",
            f"Phone:         {data.get('Phone_number', '')}",
            f"Grade Level:   {data.get('Grade_level', '')}",
            f"Strand:        {data.get('Strand', '')}",
            f"Semester:      {data.get('Semester', '')}",
            f"Prev. School:  {data.get('Previous_school', '')}",
            f"Guardian:      {data.get('Guardian_First_name', '')} {data.get('Guardian_Last_name', '')}",
            f"Guardian Ph:   {data.get('Guadian_Phone_Number', '')}",
            f"Relationship:  {data.get('Current_Relationship', '')}",
        ])
        box = QMessageBox(self)
        box.setWindowTitle(f"Student Details — {lrn}")
        box.setText(msg)
        box.exec()

    def logout(self):
        self.stack.setCurrentIndex(0)


# ══════════════════════════════════════════════════════════════════
#  ADMIN PORTAL LOGIN
# ══════════════════════════════════════════════════════════════════
class adminPortal(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        box = QWidget()
        box_layout = QVBoxLayout(box)
        box.setFixedSize(450, 550)
        box.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")

        back_btn = QPushButton('<-back')
        back_btn.clicked.connect(self.back)
        back_btn.setStyleSheet("padding: 0px;")

        logo = QLabel()
        pixmap = QPixmap("Logo.png")
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        logo.setFixedSize(150, 150)

        title = QWidget()
        title.setFixedHeight(90)
        title.setStyleSheet("padding: 1px; background: black; color: white;")
        title_layout = QVBoxLayout(title)
        title_header = QLabel("Admin Portal")
        title_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_paragraph = QLabel("System Administrator Login")
        title_paragraph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_header)
        title_layout.addWidget(title_paragraph)

        form_box = QWidget()
        form_box.setObjectName('form_box')
        form_box.setStyleSheet("""
        #form_box { background: white; border: 1px solid gray; padding: 0px; }
        #user_name, #user_pass { padding: 0px; }
        #user_name_input, #user_pass_input {
            border: 1px solid gray; margin-top: 10px; padding: 0px;
            border-radius: 4px; height: 50px; }
        #login_btn { border-radius: 4px; background: black; color: white; }
        #login_btn:hover  { background: gray; color: white; border-radius: 8px; }
        #login_btn:pressed { background: black; color: white; }
        """)
        form_box_layout = QVBoxLayout(form_box)

        user_name = QGroupBox("Username: ")
        user_name.setObjectName('user_name')
        user_name.setFixedHeight(50)
        user_name_layout = QHBoxLayout(user_name)
        self.user_name_input = QLineEdit()
        self.user_name_input.setObjectName('user_name_input')
        user_name_layout.addWidget(self.user_name_input)

        user_pass = QGroupBox("Password: ")
        user_pass.setFixedHeight(50)
        user_pass.setObjectName('user_pass')
        user_pass_layout = QHBoxLayout(user_pass)
        self.user_pass_input = QLineEdit()
        self.user_pass_input.setObjectName('user_pass_input')
        self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        user_pass_layout.addWidget(self.user_pass_input)

        self.user_pass_btn = QPushButton('Show pass')
        self.user_pass_btn.clicked.connect(self.toggle_pass)
        self.user_pass_btn.setStyleSheet("""
        padding: 0px; padding-left: 10px; border-radius: 5px;
        margin-left: 10px; margin-right: 300px;
        background: gray; color: white;
        """)

        login_btn = QPushButton('Log-in')
        login_btn.clicked.connect(
            lambda: self.go_to_admin_portal(self.user_name_input, self.user_pass_input))
        login_btn.setObjectName('login_btn')

        form_box_layout.addWidget(user_name)
        form_box_layout.addWidget(user_pass)
        form_box_layout.addWidget(self.user_pass_btn)
        form_box_layout.addWidget(login_btn)

        box_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        box_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        box_layout.addWidget(title)
        box_layout.addWidget(form_box, 2)
        main_layout.addWidget(box)
        self.setLayout(main_layout)

    def toggle_pass(self):
        if self.user_pass_input.echoMode() == QLineEdit.EchoMode.Password:
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.user_pass_btn.setText("Hide pass ")
        else:
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.user_pass_btn.setText("Show pass")

    def back(self):
        self.stack.setCurrentIndex(0)

    def go_to_admin_portal(self, name, password):
        user = name.text().strip()
        pas = password.text().strip()

        if not user or not pas:
            QMessageBox.warning(self, "Login Failed", "Please enter your credentials.")
            return

        log = login(user, pas)
        result = log.check_pass_admin()

        if result == 'approved':
            self.user_pass_input.clear()
            self.user_name_input.clear()
            self.user_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            portal: adminPortalAccount = self.stack.widget(7)
            portal.refresh_all()
            self.stack.setCurrentIndex(7)
        elif result in ('not_found', 'wrong_password'):
            QMessageBox.critical(self, "Login Failed", "These credentials do not match our records.")
        else:
            QMessageBox.critical(self, "Error", "An error occurred. Please try again.")


# ══════════════════════════════════════════════════════════════════
#  HELPER
# ══════════════════════════════════════════════════════════════════
def _pct(part: int, total: int) -> int:
    return part * 100 // total if total else 0


# ══════════════════════════════════════════════════════════════════
#  ADMIN DASHBOARD CHART  — bar (strands) + pie (enrolled this week)
# ══════════════════════════════════════════════════════════════════
class DashboardChartWidget(QWebEngineView):
    STRAND_COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#8b5cf6']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(520)
        self._data = {}
        self._render()

    def update_data(self, counts: dict, students: list[dict], weekly: dict):
        strand_counts: dict[str, int] = {}
        grade_counts: dict[str, int] = {}
        for s in students:
            strand = s.get('Strand') or 'Unknown'
            grade = s.get('Grade_level') or 'Unknown'
            strand_counts[strand] = strand_counts.get(strand, 0) + 1
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        self._data = {
            'total': sum(counts.values()),
            'strand': strand_counts,
            'grade': grade_counts,
            'this_week': weekly.get('this_week', 0),
            'before': weekly.get('before', 0),
        }
        self._render()

    def _render(self):
        total = self._data.get('total', 0)
        strand = self._data.get('strand', {})
        grade = self._data.get('grade', {})
        this_week = self._data.get('this_week', 0)
        before = self._data.get('before', 0)

        strand_cards = "".join(
            f'<div class="card" style="--c:{self.STRAND_COLORS[i % len(self.STRAND_COLORS)]}">'
            f'<div class="card-lbl">{s}</div><div class="card-val">{n}</div></div>'
            for i, (s, n) in enumerate(sorted(strand.items()))
        )
        grade_cards = "".join(
            f'<div class="card" style="--c:#64748b">'
            f'<div class="card-lbl">Grade {g}</div><div class="card-val">{n}</div></div>'
            for g, n in sorted(grade.items())
        )
        strand_labels = json.dumps(list(strand.keys()))
        strand_values = json.dumps(list(strand.values()))
        bar_colors = json.dumps([
            self.STRAND_COLORS[i % len(self.STRAND_COLORS)]
            for i in range(len(strand))
        ])

        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#f8fafc; font-family:'Segoe UI',sans-serif; padding:16px; color:#1e293b; }}
  h3 {{ font-size:12px; font-weight:700; text-transform:uppercase;
        letter-spacing:.6px; color:#94a3b8; margin-bottom:8px; margin-top:12px; }}
  .cards {{ display:flex; flex-wrap:wrap; gap:10px; margin-bottom:10px; }}
  .card {{
    background:white; border-radius:8px; padding:10px 14px;
    border-left:4px solid var(--c);
    box-shadow:0 1px 3px rgba(0,0,0,.08); min-width:80px;
  }}
  .card-lbl {{ font-size:10px; font-weight:700; color:var(--c);
               text-transform:uppercase; letter-spacing:.4px; }}
  .card-val {{ font-size:22px; font-weight:700; color:#1e293b; margin-top:2px; }}
  .charts-row {{ display:flex; gap:16px; margin-top:10px; }}
  .chart-box {{
    background:white; border-radius:10px; padding:14px 16px;
    box-shadow:0 1px 3px rgba(0,0,0,.08); flex:1;
  }}
  .chart-title {{ font-size:11px; font-weight:700; color:#475569; margin-bottom:10px;
                  text-transform:uppercase; letter-spacing:.5px; }}
  canvas {{ max-height:160px; }}
</style>
</head>
<body>


<h3>By Strand</h3>
<div class="cards">{strand_cards}</div>

<h3>By Grade Level</h3>
<div class="cards">{grade_cards}</div>

<div class="charts-row">
  <div class="chart-box">
    <div class="chart-title">Students per Strand</div>
    <canvas id="bar"></canvas>
  </div>
  <div class="chart-box">
    <div class="chart-title">Enrolled This Week</div>
    <canvas id="pie"></canvas>
  </div>
</div>

<script>
new Chart(document.getElementById('bar'), {{
  type: 'bar',
  data: {{
    labels: {strand_labels},
    datasets: [{{
      label: 'Students',
      data: {strand_values},
      backgroundColor: {bar_colors},
      borderRadius: 6,
      borderSkipped: false
    }}]
  }},
  options: {{
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 11 }} }} }},
      y: {{
        beginAtZero: true,
        ticks: {{ stepSize: 1, font: {{ size: 11 }} }},
        grid: {{ color: '#f1f5f9' }}
      }}
    }},
    animation: {{ duration: 600, easing: 'easeOutQuart' }}
  }}
}});

new Chart(document.getElementById('pie'), {{
  type: 'doughnut',
  data: {{
    labels: ['This Week', 'Before'],
    datasets: [{{
      data: [{this_week}, {before}],
      backgroundColor: ['#10b981', '#e2e8f0'],
      borderWidth: 2,
      borderColor: '#f8fafc',
      hoverOffset: 6
    }}]
  }},
  options: {{
    cutout: '55%',
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ font: {{ size: 11 }}, padding: 10 }} }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.label}}: ${{ctx.parsed}}`
        }}
      }}
    }}
  }}
}});
</script>
</body></html>"""
        self.setHtml(html, QUrl("https://cdn.jsdelivr.net"))


# ══════════════════════════════════════════════════════════════════
#  REPORT WINDOW  (PDF export)
# ══════════════════════════════════════════════════════════════════
class ReportWindow(QWidget):
    def __init__(self, counts: dict, students: list[dict], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enrollment Report — Springfield Academy")
        self.resize(960, 720)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QWidget()
        toolbar.setFixedHeight(46)
        toolbar.setStyleSheet("background:#0f172a;")
        tbl = QHBoxLayout(toolbar)
        tbl.setContentsMargins(14, 6, 14, 6)

        lbl = QLabel("📄  Enrollment Report")
        lbl.setStyleSheet("color:white; font-size:14px; font-weight:bold;")

        self._save_btn = QPushButton("💾  Save as PDF")
        self._save_btn.setFixedHeight(30)
        self._save_btn.setEnabled(False)
        self._save_btn.setStyleSheet("""
            QPushButton          { background:#4f46e5; color:white; border-radius:4px; padding:0 16px; font-size:12px; }
            QPushButton:hover    { background:#3730a3; }
            QPushButton:disabled { background:#94a3b8; }
        """)

        close_btn = QPushButton("✕  Close")
        close_btn.setFixedHeight(30)
        close_btn.setStyleSheet("""
            QPushButton       { background:#ef4444; color:white; border-radius:4px; padding:0 14px; font-size:12px; }
            QPushButton:hover { background:#b91c1c; }
        """)
        close_btn.clicked.connect(self.close)

        tbl.addWidget(lbl)
        tbl.addStretch()
        tbl.addWidget(self._save_btn)
        tbl.addWidget(close_btn)

        self._view = QWebEngineView()
        self._view.setHtml(self._build_html(counts, students), QUrl("https://cdn.jsdelivr.net"))
        self._view.loadFinished.connect(
            lambda _: QTimer.singleShot(900, lambda: self._save_btn.setEnabled(True))
        )
        self._save_btn.clicked.connect(self._save_pdf)

        layout.addWidget(toolbar)
        layout.addWidget(self._view, 1)

    def _save_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Report as PDF",
            os.path.join(os.path.expanduser("~"), f"enrollment_report_{date.today()}.pdf"),
            "PDF Files (*.pdf)"
        )
        if not path:
            return

        self._save_btn.setEnabled(False)
        self._save_btn.setText("⏳  Saving…")

        def _on_done(file_path: str):
            self._save_btn.setEnabled(True)
            self._save_btn.setText("💾  Save as PDF")
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                QMessageBox.information(self, "Saved", f"Report saved to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Error", "PDF was not created. Please try again.")

        self._view.page().printToPdf(path)
        QTimer.singleShot(3000, lambda: _on_done(path))

    @staticmethod
    def _build_html(counts: dict, students: list[dict]) -> str:
        p = counts.get('Pending', 0)
        a = counts.get('Approved', 0)
        d = counts.get('Declined', 0)
        total = p + a + d or 1
        today = date.today().strftime("%B %d, %Y")

        strand_counts: dict[str, int] = {}
        grade_counts: dict[str, int] = {}
        for s in students:
            k = s.get('Strand') or 'Unknown'
            g = s.get('Grade_level') or 'Unknown'
            strand_counts[k] = strand_counts.get(k, 0) + 1
            grade_counts[g] = grade_counts.get(g, 0) + 1

        strand_stat_cards = "".join(
            f'<div class="card" style="--c:#4f46e5">'
            f'<div class="card-lbl">{s}</div><div class="card-val">{n}</div></div>'
            for s, n in sorted(strand_counts.items())
        )
        grade_stat_cards = "".join(
            f'<div class="card" style="--c:#64748b">'
            f'<div class="card-lbl">Grade {g}</div><div class="card-val">{n}</div></div>'
            for g, n in sorted(grade_counts.items())
        )
        strand_rows = "".join(
            f"<tr><td>{s}</td><td>{n}</td><td>{_pct(n, total)}%</td></tr>"
            for s, n in sorted(strand_counts.items(), key=lambda x: -x[1])
        )
        recent = students[:15]
        recent_rows = "".join(
            f"""<tr>
              <td>{s.get('student_lrn', '')}</td>
              <td>{s.get('First_name', '')} {s.get('Last_name', '')}</td>
              <td>{s.get('Grade_level', '')}</td>
              <td>{s.get('Strand', '')}</td>
              <td class="st-{(s.get('Status') or 'pending').lower()}">{s.get('Status', '')}</td>
            </tr>"""
            for s in recent
        )
        strand_labels = json.dumps(list(strand_counts.keys()))
        strand_data = json.dumps(list(strand_counts.values()))

        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'IBM Plex Sans',sans-serif;background:#f8fafc;color:#1e293b;padding:32px 36px;}}
.header{{display:flex;justify-content:space-between;align-items:flex-end;
         padding-bottom:14px;border-bottom:3px solid #0f172a;margin-bottom:24px;}}
.school{{font-size:22px;font-weight:700;}}
.sub{{font-size:12px;color:#64748b;margin-top:3px;}}
.date-lbl{{font-size:11px;color:#94a3b8;}}
.cards{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px;}}
.card{{background:white;border-radius:10px;padding:14px 18px;
       border-left:4px solid var(--c);box-shadow:0 1px 4px rgba(0,0,0,.07);min-width:80px;}}
.card-lbl{{font-size:11px;font-weight:700;color:var(--c);text-transform:uppercase;letter-spacing:.5px;}}
.card-val{{font-size:26px;font-weight:700;margin-top:2px;color:#1e293b;}}
.charts{{display:flex;gap:20px;margin-bottom:28px;}}
.chart-box{{background:white;border-radius:10px;padding:18px 20px;
            box-shadow:0 1px 4px rgba(0,0,0,.07);flex:1;}}
.chart-title{{font-size:12px;font-weight:700;color:#475569;margin-bottom:12px;
              text-transform:uppercase;letter-spacing:.5px;}}
canvas{{max-height:200px;}}
.sec{{font-size:13px;font-weight:700;color:#0f172a;margin-bottom:10px;
      padding-left:10px;border-left:3px solid #4f46e5;}}
table{{width:100%;border-collapse:collapse;background:white;border-radius:10px;
       overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.07);margin-bottom:24px;}}
th{{background:#0f172a;color:white;padding:9px 12px;font-size:11px;text-align:left;font-weight:600;}}
td{{padding:8px 12px;font-size:12px;border-bottom:1px solid #f1f5f9;}}
tr:last-child td{{border-bottom:none;}}
tr:nth-child(even) td{{background:#f8fafc;}}
.st-approved{{color:#10b981;font-weight:700;}}
.st-pending{{color:#f59e0b;font-weight:700;}}
.st-declined{{color:#ef4444;font-weight:700;}}
</style></head>
<body>

<div class="header">
  <div>
    <div class="school">Springfield Academy</div>
    <div class="sub">Student Enrollment Summary Report</div>
  </div>
  <div class="date-lbl">Generated: {today}</div>
</div>

<div class="sec">Enrollment Status</div>
<div class="cards">
  <div class="card" style="--c:#1e293b"><div class="card-lbl">Total</div><div class="card-val">{total}</div></div>
  <div class="card" style="--c:#f59e0b"><div class="card-lbl">Pending</div><div class="card-val">{p}</div></div>
  <div class="card" style="--c:#10b981"><div class="card-lbl">Approved</div><div class="card-val">{a}</div></div>
  <div class="card" style="--c:#ef4444"><div class="card-lbl">Declined</div><div class="card-val">{d}</div></div>
</div>

<div class="sec">Total per Strand</div>
<div class="cards">{strand_stat_cards}</div>

<div class="sec">Total per Grade Level</div>
<div class="cards">{grade_stat_cards}</div>

<div class="charts">
  <div class="chart-box">
    <div class="chart-title">Enrollment Status</div>
    <canvas id="statusChart"></canvas>
  </div>
  <div class="chart-box">
    <div class="chart-title">Students by Strand</div>
    <canvas id="strandChart"></canvas>
  </div>
</div>

<div class="sec">Strand Breakdown</div>
<table>
  <thead><tr><th>Strand</th><th>Count</th><th>Share</th></tr></thead>
  <tbody>{strand_rows}</tbody>
</table>

<div class="sec">Student Records (latest {len(recent)})</div>
<table>
  <thead><tr><th>LRN</th><th>Name</th><th>Grade</th><th>Strand</th><th>Status</th></tr></thead>
  <tbody>{recent_rows}</tbody>
</table>

<script>
new Chart(document.getElementById('statusChart'),{{
  type:'doughnut',
  data:{{
    labels:['Pending','Approved','Declined'],
    datasets:[{{
      data:[{p},{a},{d}],
      backgroundColor:['#f59e0b','#10b981','#ef4444'],
      borderWidth:2,borderColor:'#f8fafc',hoverOffset:6
    }}]
  }},
  options:{{
    cutout:'58%',
    plugins:{{
      legend:{{position:'bottom',labels:{{font:{{size:11}},padding:12}}}},
      tooltip:{{callbacks:{{label:ctx=>`  ${{ctx.label}}: ${{ctx.parsed}} (${{Math.round(ctx.parsed*100/{total})}}%)`}}}}
    }}
  }}
}});
new Chart(document.getElementById('strandChart'),{{
  type:'bar',
  data:{{
    labels:{strand_labels},
    datasets:[{{
      label:'Students',data:{strand_data},
      backgroundColor:'#4f46e5',borderRadius:5,borderSkipped:false
    }}]
  }},
  options:{{
    plugins:{{legend:{{display:false}}}},
    scales:{{
      x:{{grid:{{display:false}},ticks:{{font:{{size:10}}}}}},
      y:{{beginAtZero:true,ticks:{{stepSize:1,font:{{size:10}}}},grid:{{color:'#f1f5f9'}}}}
    }}
  }}
}});
</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════════
#  ADMIN PORTAL ACCOUNT
# ══════════════════════════════════════════════════════════════════
class adminPortalAccount(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self._report_win = None
        self._admin_rows: list[dict] = []

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Header ──
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet('background:#0f172a;')
        hl = QHBoxLayout(header)
        hl.setContentsMargins(16, 0, 16, 0)

        logo = QLabel()
        pix = QPixmap('Logo.png')
        logo.setPixmap(pix)
        logo.setScaledContents(True)
        logo.setFixedSize(50, 50)

        title_lbl = QLabel('Springfield Academy — Admin Portal')
        title_lbl.setStyleSheet(
            'color:white;font-size:16px;font-weight:bold;background:transparent;')

        logout_btn = QPushButton('Logout')
        logout_btn.setFixedSize(80, 30)
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton      { background:#ef4444; color:white; border-radius:4px; }
            QPushButton:hover{ background:#b91c1c; }
        """)

        hl.addWidget(logo)
        hl.addWidget(title_lbl, 1)
        hl.addWidget(logout_btn)

        # ── Inner stack ──
        self.inner_stack = QStackedWidget()
        self.dash_page = self._make_dashboard_page()
        self.students_page = self._make_students_page()
        self.announce_page = self._make_announcements_page()
        self.inner_stack.addWidget(self.dash_page)  # 0
        self.inner_stack.addWidget(self.students_page)  # 1
        self.inner_stack.addWidget(self.announce_page)  # 2

        # ── Sidebar ──
        body = QWidget()
        body.setStyleSheet('background:#f8fafc;')
        bl = QHBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(0)

        sidebar = QWidget()
        sidebar.setFixedWidth(160)
        sidebar.setStyleSheet('background:#1e293b;')
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(8, 16, 8, 16)
        sl.setSpacing(6)
        sl.setAlignment(Qt.AlignmentFlag.AlignTop)

        nav_style = """
            QPushButton        { background:transparent; color:#cbd5e1; border-radius:6px;
                                 padding:8px 12px; font-size:13px; text-align:left; }
            QPushButton:hover  { background:#334155; color:white; }
            QPushButton:pressed{ background:#4f46e5; color:white; }
        """
        for label, slot in [
            ('📊  Dashboard', lambda: self.inner_stack.setCurrentIndex(0)),
            ('🎓  Students', lambda: self.inner_stack.setCurrentIndex(1)),
            ('📢  Announcements', lambda: self.inner_stack.setCurrentIndex(2)),
            ('📄  Generate Report', self._open_report),
        ]:
            b = QPushButton(label)
            b.setStyleSheet(nav_style)
            b.clicked.connect(slot)
            sl.addWidget(b)

        bl.addWidget(sidebar)
        bl.addWidget(self.inner_stack, 1)

        main_layout.addWidget(header)
        main_layout.addWidget(body, 1)

    # ── Dashboard page ────────────────────────────────────────────────
    def _make_dashboard_page(self):
        page = QWidget()
        page.setStyleSheet('background:#f8fafc;')
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        heading = QLabel('Dashboard Overview')
        heading.setStyleSheet('font-size:20px; font-weight:bold; color:#1e293b;')
        layout.addWidget(heading)

        self.dash_chart = DashboardChartWidget()
        layout.addWidget(self.dash_chart)
        layout.addStretch()
        return page

    # ── Students page ─────────────────────────────────────────────────
    def _make_students_page(self):
        page = QWidget()
        page.setStyleSheet('background:#f8fafc;')
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        heading = QLabel('Student Management')
        heading.setStyleSheet('font-size:18px; font-weight:bold; color:#1e293b;')
        layout.addWidget(heading)

        tb = QWidget()
        tb.setStyleSheet('background:transparent;')
        tbl = QHBoxLayout(tb)
        tbl.setContentsMargins(0, 0, 0, 0)

        self.admin_search = QLineEdit()
        self.admin_search.setPlaceholderText('Search students…')
        self.admin_search.setFixedWidth(220)
        self.admin_search.textChanged.connect(self._admin_search_fn)

        self.admin_filter = QComboBox()
        self.admin_filter.addItems(['All', 'Pending', 'Approved', 'Declined'])
        self.admin_filter.currentTextChanged.connect(self._admin_filter_fn)

        refresh_btn = QPushButton('⟳ Refresh')
        refresh_btn.clicked.connect(self._refresh_students)
        refresh_btn.setStyleSheet("""
            QPushButton      { background:#4f46e5; color:white; border-radius:4px; padding:4px 12px; }
            QPushButton:hover{ background:#3730a3; }
        """)

        filter_lbl = QLabel('Filter:')
        tbl.addWidget(filter_lbl)
        tbl.addWidget(self.admin_filter)
        tbl.addSpacing(8)
        tbl.addWidget(self.admin_search)
        tbl.addStretch()
        tbl.addWidget(refresh_btn)
        layout.addWidget(tb)

        self.admin_table = QTableWidget()
        self.admin_table.setColumnCount(8)
        self.admin_table.setHorizontalHeaderLabels(
            ['LRN', 'First Name', 'Last Name', 'Grade', 'Strand', 'Semester', 'Email', 'Status'])
        self.admin_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.admin_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.admin_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.admin_table.setAlternatingRowColors(True)
        self.admin_table.setStyleSheet("""
            QTableWidget { background:white; gridline-color:#e5e7eb; }
            QHeaderView::section { background:#0f172a; color:white; padding:6px; font-weight:bold; }
            QTableWidget::item:selected { background:#e0e7ff; color:#1e293b; }
        """)
        layout.addWidget(self.admin_table, 1)

        ab = QWidget()
        ab.setStyleSheet('background:transparent;')
        al = QHBoxLayout(ab)
        al.setContentsMargins(0, 4, 0, 0)

        approve_btn = QPushButton('✅ Approve')
        decline_btn = QPushButton('❌ Decline')
        delete_btn = QPushButton('🗑 Delete')
        view_btn = QPushButton('👁 Details')

        approve_btn.setStyleSheet(
            "background:#10b981;color:white;border-radius:4px;padding:6px 14px;")
        decline_btn.setStyleSheet(
            "background:#ef4444;color:white;border-radius:4px;padding:6px 14px;")
        delete_btn.setStyleSheet(
            "background:#64748b;color:white;border-radius:4px;padding:6px 14px;")
        view_btn.setStyleSheet(
            "background:#4f46e5;color:white;border-radius:4px;padding:6px 14px;")

        approve_btn.clicked.connect(lambda: self._admin_change_status('Approved'))
        decline_btn.clicked.connect(lambda: self._admin_change_status('Declined'))
        delete_btn.clicked.connect(self._admin_delete)
        view_btn.clicked.connect(self._admin_view_details)

        for b in [approve_btn, decline_btn, delete_btn, view_btn]:
            al.addWidget(b)
        al.addStretch()

        self.admin_status_lbl = QLabel('')
        self.admin_status_lbl.setStyleSheet('color:#6b7280; font-size:11px;')
        al.addWidget(self.admin_status_lbl)
        layout.addWidget(ab)
        return page

    # ── Announcements page ────────────────────────────────────────────
    def _make_announcements_page(self):
        page = QWidget()
        page.setStyleSheet('background:#f8fafc;')
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        heading = QLabel('Announcements')
        heading.setStyleSheet('font-size:18px; font-weight:bold; color:#1e293b;')
        layout.addWidget(heading)

        # ── Post new announcement ──
        compose_box = QGroupBox('Post New Announcement')
        compose_box.setStyleSheet("""
            QGroupBox { background: white; border: 1px solid #e5e7eb;
                        border-radius: 8px; padding: 10px; font-weight: bold; }
        """)
        compose_layout = QVBoxLayout(compose_box)

        title_row = QHBoxLayout()
        title_lbl = QLabel('Title:')
        title_lbl.setFixedWidth(60)
        self.ann_title_input = QLineEdit()
        self.ann_title_input.setPlaceholderText('Announcement title…')
        self.ann_title_input.setStyleSheet(
            "border: 1px solid #d1d5db; border-radius: 4px; padding: 4px 8px;")
        title_row.addWidget(title_lbl)
        title_row.addWidget(self.ann_title_input)

        target_row = QHBoxLayout()
        target_lbl = QLabel('Target:')
        target_lbl.setFixedWidth(60)
        self.ann_target_combo = QComboBox()
        self.ann_target_combo.addItems(['All', 'Student', 'Staff'])
        self.ann_target_combo.setStyleSheet(
            "border: 1px solid #d1d5db; border-radius: 4px; padding: 4px 8px; min-width: 120px;")
        target_row.addWidget(target_lbl)
        target_row.addWidget(self.ann_target_combo)
        target_row.addStretch()

        content_lbl = QLabel('Content:')
        self.ann_content_input = QTextEdit()
        self.ann_content_input.setFixedHeight(80)
        self.ann_content_input.setPlaceholderText('Write the announcement content here…')
        self.ann_content_input.setStyleSheet(
            "border: 1px solid #d1d5db; border-radius: 4px; padding: 4px 8px;")

        post_btn = QPushButton('📢  Post Announcement')
        post_btn.setStyleSheet("""
            QPushButton      { background:#4f46e5; color:white; border-radius:4px; padding:6px 16px; }
            QPushButton:hover{ background:#3730a3; }
        """)
        post_btn.clicked.connect(self._post_announcement)

        compose_layout.addLayout(title_row)
        compose_layout.addLayout(target_row)
        compose_layout.addWidget(content_lbl)
        compose_layout.addWidget(self.ann_content_input)
        compose_layout.addWidget(post_btn)
        layout.addWidget(compose_box)

        # ── Existing announcements list ──
        list_header = QHBoxLayout()
        list_lbl = QLabel('Posted Announcements')
        list_lbl.setStyleSheet('font-size:14px; font-weight:bold; color:#1e293b;')
        refresh_ann_btn = QPushButton('⟳ Refresh')
        refresh_ann_btn.setStyleSheet("""
            QPushButton      { background:#4f46e5; color:white; border-radius:4px; padding:4px 10px; }
            QPushButton:hover{ background:#3730a3; }
        """)
        refresh_ann_btn.clicked.connect(self._refresh_announcements)
        list_header.addWidget(list_lbl)
        list_header.addStretch()
        list_header.addWidget(refresh_ann_btn)
        layout.addLayout(list_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        self._ann_list_container = QWidget()
        self._ann_list_container.setStyleSheet("background: transparent;")
        self._ann_list_layout = QVBoxLayout(self._ann_list_container)
        self._ann_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._ann_list_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self._ann_list_container)
        layout.addWidget(scroll, 1)
        return page

    def _post_announcement(self):
        title = self.ann_title_input.text().strip()
        content = self.ann_content_input.toPlainText().strip()
        target = self.ann_target_combo.currentText()

        if not title or not content:
            QMessageBox.warning(self, "Incomplete", "Please fill in both title and content.")
            return

        ann = Announcement(title, content, target, posted_by='admin')
        if ann.post():
            QMessageBox.information(self, "Posted", "Announcement posted successfully.")
            self.ann_title_input.clear()
            self.ann_content_input.clear()
            self._refresh_announcements()
        else:
            QMessageBox.critical(self, "Error", "Failed to post announcement.")

    def _refresh_announcements(self):
        # Clear existing
        while self._ann_list_layout.count():
            child = self._ann_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        announcements = Announcement.get_all()
        if not announcements:
            lbl = QLabel('No announcements yet.')
            lbl.setStyleSheet('color: #6b7280; font-size: 12px;')
            self._ann_list_layout.addWidget(lbl)
            return

        for ann in announcements:
            card = QWidget()
            card.setStyleSheet("""
                background: white; border-radius: 6px;
                border-left: 4px solid #4f46e5; margin-bottom: 6px;
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 10, 8)

            top_row = QHBoxLayout()
            title_lbl = QLabel(ann.get('title', ''))
            title_lbl.setStyleSheet(
                'color: #1e293b; font-size: 13px; font-weight: bold; background: transparent;')

            date_str = str(ann.get('posted_date', ''))[:16]
            target_str = ann.get('target', '')
            meta_lbl = QLabel(f"Posted: {date_str}  |  To: {target_str}")
            meta_lbl.setStyleSheet('color: #6b7280; font-size: 10px; background: transparent;')

            ann_id = ann.get('id')
            del_btn = QPushButton('🗑')
            del_btn.setFixedSize(28, 24)
            del_btn.setStyleSheet("""
                QPushButton      { background:#ef4444; color:white; border-radius:4px; font-size:11px; }
                QPushButton:hover{ background:#b91c1c; }
            """)
            del_btn.clicked.connect(lambda _, aid=ann_id: self._delete_announcement(aid))

            top_row.addWidget(title_lbl)
            top_row.addStretch()
            top_row.addWidget(del_btn)

            content_lbl = QLabel(ann.get('content', ''))
            content_lbl.setWordWrap(True)
            content_lbl.setStyleSheet('color: #374151; font-size: 11px; background: transparent;')

            card_layout.addLayout(top_row)
            card_layout.addWidget(meta_lbl)
            card_layout.addWidget(content_lbl)
            self._ann_list_layout.addWidget(card)

    def _delete_announcement(self, ann_id: int):
        if QMessageBox.question(
                self, "Delete", "Delete this announcement?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            if Announcement.delete(ann_id):
                self._refresh_announcements()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete announcement.")

    # ── Report ────────────────────────────────────────────────────────
    def _open_report(self):
        counts = Students.count_by_status()
        students = Students.get_all_students()
        self._report_win = ReportWindow(counts, students)
        self._report_win.show()

    # ── Refresh ───────────────────────────────────────────────────────
    def refresh_all(self):
        self._refresh_students()
        self._refresh_dashboard()
        self._refresh_announcements()

    def _refresh_dashboard(self):
        counts = Students.count_by_status()
        students = Students.get_all_students()
        weekly = Students.count_enrolled_this_week()
        self.dash_chart.update_data(counts, students, weekly)

    def _refresh_students(self):
        self._admin_rows = Students.get_all_students()
        self._admin_populate(self._admin_rows)

    def _admin_populate(self, rows: list[dict]):
        self.admin_table.setRowCount(0)
        for row_data in rows:
            r = self.admin_table.rowCount()
            self.admin_table.insertRow(r)
            cols = ['student_lrn', 'First_name', 'Last_name',
                    'Grade_level', 'Strand', 'Semester', 'Email_address', 'Status']
            for c, col in enumerate(cols):
                val = row_data.get(col, '') or ''
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 'Status':
                    cm = {'Pending': '#fef3c7', 'Approved': '#d1fae5', 'Declined': '#fee2e2'}
                    item.setBackground(QColor(cm.get(str(val), 'white')))
                self.admin_table.setItem(r, c, item)
        self.admin_status_lbl.setText(f'{len(rows)} record(s)')

    def _admin_selected_lrn(self) -> str | None:
        row = self.admin_table.currentRow()
        item = self.admin_table.item(row, 0) if row >= 0 else None
        return item.text() if item else None

    def _admin_search_fn(self, text):
        results = Students.search_students(text.strip()) if text.strip() else self._admin_rows
        f = self.admin_filter.currentText()
        if f != 'All':
            results = [r for r in results if r.get('Status') == f]
        self._admin_populate(results)

    def _admin_filter_fn(self, value):
        base = self._admin_rows if value == 'All' else \
            [r for r in self._admin_rows if r.get('Status') == value]
        kw = self.admin_search.text().strip()
        if kw:
            base = [r for r in base if kw.lower() in str(r).lower()]
        self._admin_populate(base)

    def _admin_change_status(self, new_status: str):
        lrn = self._admin_selected_lrn()
        if not lrn:
            QMessageBox.warning(self, "No Selection", "Please select a student first.")
            return
        if Students.update_student_status(lrn, new_status):
            QMessageBox.information(self, "Updated", f"Status set to '{new_status}'.")
            self.refresh_all()
        else:
            QMessageBox.critical(self, "Error", "Failed to update status.")

    def _admin_delete(self):
        lrn = self._admin_selected_lrn()
        if not lrn:
            QMessageBox.warning(self, "No Selection", "Please select a student first.")
            return
        if QMessageBox.question(
                self, "Confirm Delete", f"Delete student {lrn}? This cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            if Students.delete_student(lrn):
                QMessageBox.information(self, "Deleted", f"Student {lrn} removed.")
                self.refresh_all()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete student.")

    def _admin_view_details(self):
        lrn = self._admin_selected_lrn()
        if not lrn:
            QMessageBox.warning(self, "No Selection", "Please select a student first.")
            return
        data = Students.get_student_by_lrn(lrn)
        if not data:
            QMessageBox.warning(self, "Not Found", "Could not retrieve student data.")
            return
        msg = "\n".join([
            f"LRN:           {data.get('student_lrn', '')}",
            f"Name:          {data.get('First_name', '')} {data.get('Middle_name', '')} {data.get('Last_name', '')}",
            f"Date of Birth: {data.get('Date_of_birth', '')}",
            f"Gender:        {data.get('Gender', '')}",
            f"Email:         {data.get('Email_address', '')}",
            f"Phone:         {data.get('Phone_number', '')}",
            f"Grade Level:   {data.get('Grade_level', '')}",
            f"Strand:        {data.get('Strand', '')}",
            f"Semester:      {data.get('Semester', '')}",
            f"Prev. School:  {data.get('Previous_school', '')}",
            f"Guardian:      {data.get('Guardian_First_name', '')} {data.get('Guardian_Last_name', '')}",
            f"Guardian Ph:   {data.get('Guadian_Phone_Number', '')}",
            f"Relationship:  {data.get('Current_Relationship', '')}",
        ])
        box = QMessageBox(self)
        box.setWindowTitle(f"Student Details — {lrn}")
        box.setText(msg)
        box.exec()

    def logout(self):
        self.stack.setCurrentIndex(0)


# ══════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Springfield Academy — Enrollment System")

        self.stack = QStackedWidget()

        self.login = LoginPage(self.stack)
        self.student = studentPortal(self.stack)
        self.student_portal_account = StudentPortalAccount(self.stack)
        self.student_form = StudentForm(self.stack)
        self.staff = staffPortal(self.stack)
        self.admin = adminPortal(self.stack)
        self.staff_account = StaffPortalAccount(self.stack)
        self.admin_account = adminPortalAccount(self.stack)

        self.stack.addWidget(self.login)  # 0
        self.stack.addWidget(self.student)  # 1
        self.stack.addWidget(self.student_portal_account)  # 2
        self.stack.addWidget(self.student_form)  # 3
        self.stack.addWidget(self.staff)  # 4
        self.stack.addWidget(self.admin)  # 5
        self.stack.addWidget(self.staff_account)  # 6
        self.stack.addWidget(self.admin_account)  # 7

        self.setCentralWidget(self.stack)


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
window.show()
sys.exit(app.exec())