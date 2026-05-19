import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
import Admin

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Example")
        self.setFixedSize(300, 200)



