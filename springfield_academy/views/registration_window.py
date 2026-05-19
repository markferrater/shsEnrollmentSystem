import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QGroupBox,
    QMessageBox, QScrollArea, QStackedWidget
)
from PyQt6.QtCore import Qt, QDate
import bcrypt
from styles.theme import APP_STYLE, COLORS
from database_conn import database


class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Springfield Academy — Student Registration")
        self.setMinimumSize(780, 620)
        self.setStyleSheet(APP_STYLE)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page1 = self._build_personal_info()
        self.page2 = self._build_enrollment_info()

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

    # ─── Page 1: Personal Info ──────────────────────────────────
    def _build_personal_info(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #F0F4F8; }")

        container = QWidget()
        container.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Header
        hdr = QLabel("Student Registration")
        hdr.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {COLORS['primary']};")
        step = QLabel("Step 1 of 2 — Personal Information")
        step.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")

        # Personal info group
        grp = QGroupBox("Personal Information")
        grid = QGridLayout(grp)
        grid.setSpacing(10)

        self.fname = QLineEdit(); self.fname.setPlaceholderText("First Name")
        self.mname = QLineEdit(); self.mname.setPlaceholderText("Middle Name")
        self.lname = QLineEdit(); self.lname.setPlaceholderText("Last Name")
        self.dob = QDateEdit(); self.dob.setCalendarPopup(True); self.dob.setDate(QDate(2006, 1, 1))
        self.gender = QComboBox(); self.gender.addItems(["Male", "Female", "Prefer not to say"])
        self.email = QLineEdit(); self.email.setPlaceholderText("Email Address")
        self.phone = QLineEdit(); self.phone.setPlaceholderText("Phone Number")
        self.address = QLineEdit(); self.address.setPlaceholderText("Complete Address")

        grid.addWidget(QLabel("First Name *"), 0, 0); grid.addWidget(self.fname, 0, 1)
        grid.addWidget(QLabel("Middle Name"), 0, 2); grid.addWidget(self.mname, 0, 3)
        grid.addWidget(QLabel("Last Name *"), 1, 0); grid.addWidget(self.lname, 1, 1)
        grid.addWidget(QLabel("Date of Birth *"), 1, 2); grid.addWidget(self.dob, 1, 3)
        grid.addWidget(QLabel("Gender"), 2, 0); grid.addWidget(self.gender, 2, 1)
        grid.addWidget(QLabel("Email *"), 2, 2); grid.addWidget(self.email, 2, 3)
        grid.addWidget(QLabel("Phone"), 3, 0); grid.addWidget(self.phone, 3, 1)
        grid.addWidget(QLabel("Address"), 3, 2); grid.addWidget(self.address, 3, 3)

        # Guardian group
        g2 = QGroupBox("Parent / Guardian Information")
        g2grid = QGridLayout(g2)
        g2grid.setSpacing(10)

        self.gfname = QLineEdit(); self.gfname.setPlaceholderText("First Name")
        self.gmname = QLineEdit(); self.gmname.setPlaceholderText("Middle Name")
        self.glname = QLineEdit(); self.glname.setPlaceholderText("Last Name")
        self.gphone = QLineEdit(); self.gphone.setPlaceholderText("Phone Number")
        self.grel = QComboBox()
        self.grel.addItems(["Father", "Mother", "Guardian", "Sibling", "Other"])

        g2grid.addWidget(QLabel("First Name *"), 0, 0); g2grid.addWidget(self.gfname, 0, 1)
        g2grid.addWidget(QLabel("Middle Name"), 0, 2); g2grid.addWidget(self.gmname, 0, 3)
        g2grid.addWidget(QLabel("Last Name *"), 1, 0); g2grid.addWidget(self.glname, 1, 1)
        g2grid.addWidget(QLabel("Phone *"), 1, 2); g2grid.addWidget(self.gphone, 1, 3)
        g2grid.addWidget(QLabel("Relation"), 2, 0); g2grid.addWidget(self.grel, 2, 1)

        next_btn = QPushButton("Next →")
        next_btn.clicked.connect(self._go_page2)

        layout.addWidget(hdr)
        layout.addWidget(step)
        layout.addWidget(grp)
        layout.addWidget(g2)
        layout.addWidget(next_btn, alignment=Qt.AlignmentFlag.AlignRight)

        scroll.setWidget(container)
        return scroll

    # ─── Page 2: Enrollment Info ────────────────────────────────
    def _build_enrollment_info(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #F0F4F8; }")

        container = QWidget()
        container.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        hdr = QLabel("Student Registration")
        hdr.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {COLORS['primary']};")
        step = QLabel("Step 2 of 2 — Enrollment & Account Setup")
        step.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")

        grp = QGroupBox("Academic Information")
        grid = QGridLayout(grp)
        grid.setSpacing(10)

        self.grade_level = QComboBox()
        self.grade_level.addItems(["Grade 11", "Grade 12"])
        self.strand = QComboBox()
        self.strand.addItems(["STEM", "ABM", "HUMSS", "GAS", "TVL", "Sports", "Arts & Design"])
        self.prev_school = QLineEdit(); self.prev_school.setPlaceholderText("Previous School Name")
        self.school_year = QComboBox()
        self.school_year.addItems(["2025-2026", "2026-2027", "2027-2028"])

        grid.addWidget(QLabel("Grade Level *"), 0, 0); grid.addWidget(self.grade_level, 0, 1)
        grid.addWidget(QLabel("Strand *"), 0, 2); grid.addWidget(self.strand, 0, 3)
        grid.addWidget(QLabel("Previous School"), 1, 0); grid.addWidget(self.prev_school, 1, 1)
        grid.addWidget(QLabel("School Year"), 1, 2); grid.addWidget(self.school_year, 1, 3)

        grp2 = QGroupBox("Account Credentials")
        grid2 = QGridLayout(grp2)
        grid2.setSpacing(10)

        self.new_username = QLineEdit(); self.new_username.setPlaceholderText("Choose a username")
        self.new_password = QLineEdit(); self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setPlaceholderText("Choose a password")
        self.confirm_password = QLineEdit(); self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setPlaceholderText("Confirm password")

        grid2.addWidget(QLabel("Username *"), 0, 0); grid2.addWidget(self.new_username, 0, 1)
        grid2.addWidget(QLabel("Password *"), 1, 0); grid2.addWidget(self.new_password, 1, 1)
        grid2.addWidget(QLabel("Confirm Password *"), 2, 0); grid2.addWidget(self.confirm_password, 2, 1)

        btn_row = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("outline_btn")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        submit_btn = QPushButton("Submit Application")
        submit_btn.clicked.connect(self._submit)

        btn_row.addWidget(back_btn)
        btn_row.addStretch()
        btn_row.addWidget(submit_btn)

        layout.addWidget(hdr)
        layout.addWidget(step)
        layout.addWidget(grp)
        layout.addWidget(grp2)
        layout.addLayout(btn_row)

        scroll.setWidget(container)
        return scroll

    def _go_page2(self):
        if not self.fname.text().strip() or not self.lname.text().strip() or not self.email.text().strip():
            QMessageBox.warning(self, "Missing Fields", "Please fill in the required fields (*).")
            return
        self.stack.setCurrentIndex(1)

    def _generate_lrn(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            while True:
                lrn = ''.join(str(random.randint(0, 9)) for _ in range(12))
                cur.execute("SELECT lrn_id FROM student_info WHERE lrn_id=%s", (lrn,))
                if not cur.fetchone():
                    return lrn
        finally:
            cur.close()
            conn.close()

    def _submit(self):
        username = self.new_username.text().strip()
        password = self.new_password.text()
        confirm = self.confirm_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Missing Fields", "Please fill all required fields.")
            return
        if password != confirm:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match.")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Weak Password", "Password must be at least 6 characters.")
            return

        lrn = self._generate_lrn()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO student_info
                (lrn_id, first_name, middle_name, last_name, date_of_birth, gender,
                 email, phone, address, guardian_first_name, guardian_middle_name,
                 guardian_last_name, guardian_phone, guardian_relation,
                 grade_level, strand, previous_school, school_year)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                lrn,
                self.fname.text().strip(), self.mname.text().strip(), self.lname.text().strip(),
                self.dob.date().toString("yyyy-MM-dd"), self.gender.currentText(),
                self.email.text().strip(), self.phone.text().strip(), self.address.text().strip(),
                self.gfname.text().strip(), self.gmname.text().strip(), self.glname.text().strip(),
                self.gphone.text().strip(), self.grel.currentText(),
                self.grade_level.currentText(), self.strand.currentText(),
                self.prev_school.text().strip(), self.school_year.currentText()
            ))
            cur.execute("INSERT INTO student_status (student_lrn, status) VALUES (%s, 'Pending')", (lrn,))
            cur.execute(
                "INSERT INTO student_credentials (student_lrn, username, password) VALUES (%s,%s,%s)",
                (lrn, username, hashed)
            )
            conn.commit()

            QMessageBox.information(self, "Registration Submitted! ✅",
                f"Your application has been submitted successfully!\n\n"
                f"Your LRN: {lrn}\n"
                f"Username: {username}\n\n"
                f"Please wait for staff approval before logging in.")
            self.close()
        except Exception as e:
            conn.rollback()
            if 'Duplicate entry' in str(e) and 'username' in str(e):
                QMessageBox.warning(self, "Username Taken", "That username is already taken. Please choose another.")
            else:
                QMessageBox.critical(self, "Error", f"Registration failed:\n{e}")
        finally:
            cur.close()
            conn.close()
