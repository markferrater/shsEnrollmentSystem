import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QGroupBox, QLineEdit, QScrollBar
)
from PyQt6.QtCore import Qt

class main(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(730,410)

        #Main layout
        main_layout = QVBoxLayout()


        # Top content
        top = QHBoxLayout()

        top_content_logo = QHBoxLayout()
        label_logo = QLabel('Logo pic')

        top_content_logo.addWidget(label_logo)

        top_content_logo_side = QVBoxLayout()
        label_logo_text1 = QLabel('hello')
        label_logo_text2 = QLabel('world')

        top_content_logo_side.addWidget(label_logo_text1)
        top_content_logo_side.addWidget(label_logo_text2)


        top_content_logout = QHBoxLayout()
        label_logout = QLabel("logout")
        label_logout.setStyleSheet("""
        background-color: red;
        """)

        #adjusting the text inside of the layout
        label_logout.setContentsMargins(150,5,10,5)



        top_content_logout.addWidget(label_logout)





        # Bottom content
        bottom = QVBoxLayout()

        letter = QLabel('bottom content')






        top.addLayout(top_content_logo)
        top.addLayout(top_content_logo_side)
        top.addLayout(top_content_logout)

        bottom.addWidget(letter)

        main_layout.addLayout(top)
        main_layout.addLayout(bottom)

        self.setLayout(main_layout)








if __name__ == "__main__":
    app = QApplication([])
    window = main()
    window.show()
    sys.exit(app.exec())
