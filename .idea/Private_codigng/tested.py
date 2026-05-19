from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

frame1 = QWidget()
f1_layout = QVBoxLayout(frame1)
btn1 = QPushButton("Go to Frame 2")
f1_layout.addWidget(btn1)

frame2 = QWidget()
f2_layout = QVBoxLayout(frame2)
btn2 = QPushButton("Back to Frame 1")
f2_layout.addWidget(btn2)

layout.addWidget(frame1)
layout.addWidget(frame2)

frame2.hide()  # hide second frame initially

btn1.clicked.connect(lambda: (frame1.hide(), frame2.show()))
btn2.clicked.connect(lambda: (frame2.hide(), frame1.show()))

window.show()
sys.exit(app.exec())
