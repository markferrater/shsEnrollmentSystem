import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
import Admin
from testing.testing import window


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 500)

        # ===== Main Layout =====
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Login Card (Frame) =====
        self.card = QFrame()
        self.card.setObjectName("loginCard")
        self.card.setFixedWidth(320)
        self.card.setStyleSheet("""
            border-radius: 15px;
        
        
        """)

        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(16)

        # ===== Title =====
        title = QLabel("Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            background-color: white;
        """)

        # ===== Username =====
        self.username = self.labeled_input("Username")

        # ===== Password =====
        self.password = self.labeled_input("Password", password=True)

        # ===== Login Button =====
        self.login_btn = QPushButton("Log in")
        self.login_btn.setFixedHeight(40)
        self.login_btn.clicked.connect(self.check_login)

        # ===== Message =====
        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Add widgets =====
        card_layout.addWidget(title)
        card_layout.addWidget(self.username["container"])
        card_layout.addWidget(self.password["container"])
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.message)

        main_layout.addWidget(self.card)

        # ===== Styles =====
        self.setStyleSheet(self.styles())

    # ---------- Labeled Input ----------
    def labeled_input(self, text, password=False):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setSpacing(4)

        label = QLabel(text)
        field = QLineEdit()

        if password:
            field.setEchoMode(QLineEdit.EchoMode.Password)

        label.setStyleSheet("font-size: 12px; color: #555;")
        field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
        """)

        layout.addWidget(label)
        layout.addWidget(field)

        return {"container": container, "field": field}

    # ---------- Login Logic ----------
    def check_login(self):
        user = self.username["field"].text()
        pwd = self.password["field"].text()

        if user == "admin" and pwd == "1234":
            self.message.setText("Login successful")
            self.message.setStyleSheet("color: green;")

            window = Admin.Main_Window()
            window.show()
            LoginWindow.hide()
            sys.exit(Admin.app.exec())

        else:
            self.message.setText("Invalid username or password")
            self.message.setStyleSheet("color: red;")

    # ---------- Styles ----------
    def styles(self):
        return """
        QWidget {
            background-color: #f4f6f9;
        }

        QFrame#loginCard {
            background-color: white; balck
            border-radius: 14px;
            padding: 20px;
        }

        QPushButton {
            background-color: #4a90e2;
            color: white;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #357abd;
        }

        QPushButton:pressed {
            background-color: #2c5f99;
        }
        """



