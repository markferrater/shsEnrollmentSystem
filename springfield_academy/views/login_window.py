import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon

from styles.theme import APP_STYLE, COLORS
from models.login_model import login
from views.registration_window import RegistrationWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Springfield Academy — Login")
        self.setMinimumSize(900, 580)
        self.setStyleSheet(APP_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ── Left branding panel ───────────────────────────────
        left = QWidget()
        left.setFixedWidth(380)
        left.setStyleSheet(f"background: {COLORS['primary']};")
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setSpacing(16)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Logo.png')
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pix)
        else:
            logo_label.setText("🎓")
            logo_label.setStyleSheet("font-size: 60px;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        school_name = QLabel("SPRINGFIELD\nACADEMY")
        school_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        school_name.setStyleSheet("color: white; font-size: 24px; font-weight: 800; letter-spacing: 2px;")

        tagline = QLabel("Enrollment Management System")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 13px; font-weight: 400;")

        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(255,255,255,0.2); margin: 0 40px;")

        info = QLabel("Grade 11 & 12\nSenior High School")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 12px;")

        left_layout.addStretch()
        left_layout.addWidget(logo_label)
        left_layout.addWidget(school_name)
        left_layout.addWidget(tagline)
        left_layout.addWidget(divider)
        left_layout.addWidget(info)
        left_layout.addStretch()

        # ── Right login form ──────────────────────────────────
        right = QWidget()
        right.setStyleSheet(f"background: {COLORS['light_bg']};")
        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(60, 40, 60, 40)

        form_card = QWidget()
        form_card.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 12px;
            }
        """)
        form_card.setMaximumWidth(380)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(36, 36, 36, 36)
        form_layout.setSpacing(14)

        title = QLabel("Welcome Back")
        title.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {COLORS['primary']};")

        subtitle = QLabel("Sign in to your account")
        subtitle.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; margin-bottom: 8px;")

        # Role selector
        role_label = QLabel("Login As")
        role_label.setStyleSheet(f"font-weight: 600; font-size: 12px; color: {COLORS['text_muted']};")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student", "Staff", "Admin"])
        self.role_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1.5px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px 12px;
                background: white;
                font-size: 13px;
            }}
        """)

        # Username
        user_label = QLabel("Username")
        user_label.setStyleSheet(f"font-weight: 600; font-size: 12px; color: {COLORS['text_muted']};")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")

        # Password
        pass_label = QLabel("Password")
        pass_label.setStyleSheet(f"font-weight: 600; font-size: 12px; color: {COLORS['text_muted']};")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.handle_login)

        # Login button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: white;
                border-radius: 7px;
                padding: 10px;
                font-weight: 700;
                font-size: 14px;
                min-height: 42px;
                margin-top: 6px;
            }}
            QPushButton:hover {{ background: {COLORS['secondary']}; }}
        """)
        self.login_btn.clicked.connect(self.handle_login)

        # Register link
        reg_row = QHBoxLayout()
        reg_lbl = QLabel("New student?")
        reg_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        reg_btn = QPushButton("Register here")
        reg_btn.setObjectName("outline_btn")
        reg_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['secondary']};
                border: none;
                padding: 0;
                font-size: 12px;
                font-weight: 600;
                text-decoration: underline;
                min-height: 0;
            }}
        """)
        reg_btn.clicked.connect(self.open_registration)
        reg_row.addWidget(reg_lbl)
        reg_row.addWidget(reg_btn)
        reg_row.addStretch()

        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addWidget(role_label)
        form_layout.addWidget(self.role_combo)
        form_layout.addWidget(user_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(pass_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_btn)
        form_layout.addLayout(reg_row)

        right_layout.addWidget(form_card, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(left)
        main_layout.addWidget(right, 1)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        role = self.role_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Missing Fields", "Please enter both username and password.")
            return

        auth = login(username, password)

        if role == "Student":
            result = auth.check_pass_student()
        elif role == "Staff":
            result = auth.check_pass_staff()
        else:
            result = auth.check_pass_admin()

        if result == 'approved':
            if role == "Student":
                lrn = auth.get_student_lrn()
                self._open_student_portal(lrn, username)
            elif role == "Staff":
                info = auth.get_staff_info()
                self._open_staff_portal(info, username)
            else:
                info = auth.get_admin_info()
                self._open_admin_portal(info, username)
        elif result == 'pending':
            QMessageBox.information(self, "Pending Approval",
                "Your enrollment application is still pending review.\n"
                "Please wait for the staff to approve your account.")
        elif result == 'declined':
            QMessageBox.warning(self, "Application Declined",
                "Your enrollment application has been declined.\n"
                "Please contact the school for more information.")
        elif result == 'not_found':
            QMessageBox.warning(self, "Not Found", "Username not found. Please check your credentials.")
        elif result == 'wrong_password':
            QMessageBox.warning(self, "Wrong Password", "Incorrect password. Please try again.")
        else:
            QMessageBox.critical(self, "Error", "A system error occurred. Please try again.")

    def _open_student_portal(self, lrn, username):
        from views.student_portal import StudentPortal
        self.portal = StudentPortal(lrn, username)
        self.portal.showMaximized()
        self.hide()

    def _open_staff_portal(self, info, username):
        from views.staff_portal import StaffPortal
        self.portal = StaffPortal(info, username)
        self.portal.showMaximized()
        self.hide()

    def _open_admin_portal(self, info, username):
        from views.admin_portal import AdminPortal
        self.portal = AdminPortal(info, username)
        self.portal.showMaximized()
        self.hide()

    def open_registration(self):
        self.reg_window = RegistrationWindow()
        self.reg_window.show()
