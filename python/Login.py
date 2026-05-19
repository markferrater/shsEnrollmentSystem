import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout()

        # ====== Logo ======
        label = QLabel(self)
        logo = QPixmap('logo.png')
        label.setPixmap(logo)
        label.setScaledContents(True)

        layout = QVBoxLayout()
        layout.addWidget(label)

        self.setLayout(layout)

    # ===== Frame ======
        self.card = QFrame()
        self.card.setFixedWidth(320)
        self.card.setStyleSheet("""
                    border-radius: 15px;
                """)

app = QApplication(sys.argv)
window = login()
window.show()
sys.exit(app.exec())