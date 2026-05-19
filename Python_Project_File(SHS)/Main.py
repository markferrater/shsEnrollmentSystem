import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,QPushButton, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
import Log_in
import Admin


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Example")
        self.setFixedSize(300, 200)




    def Log_out(self):
        pass


    def Admin(self):
        pass

    def Staff(self):
        pass





app = QApplication([])
window1 = Admin.admin()
window1.show()
sys.exit(app.exec())