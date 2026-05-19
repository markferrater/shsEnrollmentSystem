from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Content Example")
        self.resize(400, 300)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # ===== TOP (FIXED) =====
        self.welcome_label = QLabel("Welcome to the Application")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        main_layout.addWidget(self.welcome_label)

        # ===== BUTTONS =====
        btn_layout = QHBoxLayout()
        self.btn_user1 = QPushButton("Show User 1")
        self.btn_user2 = QPushButton("Show User 2")

        self.btn_user1.clicked.connect(
            lambda: self.show_user("Alice", 23)
        )
        self.btn_user2.clicked.connect(
            lambda: self.show_user("Bob", 30)
        )

        btn_layout.addWidget(self.btn_user1)
        btn_layout.addWidget(self.btn_user2)
        main_layout.addLayout(btn_layout)

        # ===== BOTTOM (DYNAMIC) =====
        self.content_layout = QVBoxLayout()
        main_layout.addLayout(self.content_layout)

        # initial content
        self.show_message("Press a button to show user info")

    # ----------------------------
    # Dynamic content functions
    # ----------------------------

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_message(self, text):
        self.clear_layout(self.content_layout)
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(label)

    def show_user(self, name, age):
        self.clear_layout(self.content_layout)

        name_label = QLabel(f"Name: {name}")
        age_label = QLabel(f"Age: {age}")

        self.content_layout.addWidget(name_label)
        self.content_layout.addWidget(age_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
