import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Senior High School Enrollment System")
        self.resize(900, 500)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= HEADER =================
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background-color: #7f6cf3;
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)

        logo = QLabel("SPRINGFIELD\nACADEMY")
        logo.setStyleSheet("color: white; font-weight: bold;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Senior High School Enrollment System")
        title.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: bold;
            }
        """)

        header_layout.addWidget(logo)
        header_layout.addSpacing(20)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)

        # ================= CONTENT =================
        content = QFrame()
        content.setStyleSheet("background-color: #f7f5f8;")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(30)

        # ====== CARD ROW ======
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        def create_card(title_text, btn_text):
            card = QFrame()
            card.setFixedHeight(100)
            card.setStyleSheet("""
                QFrame {
                    background-color: #dcdcdc;
                    border-radius: 12px;
                }
            """)

            layout = QHBoxLayout(card)
            layout.setContentsMargins(20, 15, 20, 15)

            text_layout = QVBoxLayout()
            title = QLabel(title_text)
            title.setStyleSheet("font-weight: bold; font-size: 14px;")
            desc = QLabel("Begin the Senior High School enrollment process by registering\nstudent information and selecting the preferred track and strand")
            desc.setStyleSheet("font-size: 10px;")

            text_layout.addWidget(title)
            text_layout.addWidget(desc)

            button = QPushButton(btn_text)
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border-radius: 10px;
                    padding: 6px 16px;
                    font-weight: bold;
                }
            """)

            layout.addLayout(text_layout)
            layout.addStretch()
            layout.addWidget(button)

            return card

        cards_layout.addWidget(create_card("Start Enrollment", "Start now"))
        cards_layout.addWidget(create_card("Show Dashboard", "Show Dashboard"))

        # ====== CENTER TEXT ======
        center_title = QLabel("Show Dashboard")
        center_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        center_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        center_text = QLabel(
            "wgaedkhjwgererjhofjewjdjrlfewerhjewprjewjr\n"
            "ererwewewewfse3refwraewrewgrderewwe"
        )
        center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Assemble content
        content_layout.addLayout(cards_layout)
        content_layout.addWidget(center_title)
        content_layout.addWidget(center_text)

        # ================= FINAL =================
        main_layout.addWidget(header)
        main_layout.addWidget(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
