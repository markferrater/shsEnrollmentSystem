from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Page1(QWidget):
    def __init__(self, switch_page):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setGeometry(0,0,500,500)
        btn = QPushButton("Go to Page 2")

        btn.clicked.connect(switch_page)
        layout.addWidget(btn)
