import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QFrame
)


class RoundedFrameExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rounded Frame Button")
        self.setFixedSize(500, 200)

        main_layout = QVBoxLayout()

        # --- Frame ---
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 15px;
                border: 2px solid #bdc3c7;
            }
        """)

        frame_layout = QVBoxLayout()

        # --- Button inside frame ---
        button = QPushButton("Login")
        button.setFixedHeight(40)
        button.setStyleSheet("""
                           QPushButton {
                               background-color: #3498db;
                               color: white;
                               font-size: 14px;
                               font-weight: bold;
                               border-radius: 10px;
                           }
                           QPushButton:hover {
                               background-color: #2980b9;
                           }
                       """)

        frame_layout.addWidget(button)
        frame.setLayout(frame_layout)

        main_layout.addWidget(frame)
        self.setLayout(main_layout)


app = QApplication(sys.argv)
window = RoundedFrameExample()
window.show()
sys.exit(app.exec())
