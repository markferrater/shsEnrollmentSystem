from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Example")
        self.setStyleSheet('background-color: white')
        self.setGeometry(100, 100, 400, 300)

        label = QLabel(self)
        pixmap = QPixmap("logo.png")

        # Resize image
        pixmap = pixmap.scaled(
            5000, 100, #200, 150
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        label.setPixmap(pixmap)
        label.move(0, 30)   # position (x, y)


        #layout = QVBoxLayout()

        #self.setLayout(layout)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
