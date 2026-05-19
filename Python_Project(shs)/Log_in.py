from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget,QPushButton, QLabel, QVBoxLayout, QHBoxLayout
import sys
import Staff

class main(QWidget):
    def __init__(self):
        super(). __init__()

        self.setWindowTitle('log in')
      #  self.setGeometry(300,100,800,500)
        self.setFixedSize(500,300)

#run/execute frame
app = QApplication([])
window = Staff.LoginWindow()
window.show()

app.exec()











