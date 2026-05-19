import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
import Staff


class Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(1350, 1000)



app = QApplication(sys.argv)
window = Staff.LoginWindow()
window.show()
sys.exit(app.exec())








