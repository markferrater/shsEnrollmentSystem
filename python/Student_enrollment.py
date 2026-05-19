import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame,
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea
)
from PyQt6.QtCore import Qt


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barangay Profiling System")
        self.resize(1200, 700)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # ===== SIDEBAR =====
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color:#0b6e3b; color:white;")

        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("Barangay Profiling\nSystem")
        title.setStyleSheet("font-size:16px; font-weight:bold;")
        sidebar_layout.addWidget(title)

        for text in ["Dashboard", "Resident Profile", "Certificates", "Reports"]:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: white;
                    text-align: left;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color:#0f8a4f;
                }
            """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # ===== MAIN CONTENT =====
        content = QWidget()
        content_layout = QVBoxLayout(content)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color:#0b6e3b; color:white;")
        header_layout = QHBoxLayout(header)

        header_title = QLabel("Barangay Profilingqwqsaqsqwqsa")
        header_title.setStyleSheet("font-size:18px; font-weight:bold;")

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("background:white; color:black; padding:5px;")

        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)

        content_layout.addWidget(header)

        # Stats Cards
        stats_layout = QHBoxLayout()

        def create_card(title, value):
            card = QFrame()
            card.setStyleSheet("""
                background:white;
                border-radius:8px;
                padding:10px;
            """)
            v = QVBoxLayout(card)
            v.addWidget(QLabel(title))
            num = QLabel(value)
            num.setStyleSheet("font-size:22px; font-weight:bold;")
            v.addWidget(num)
            return card

        stats_layout.addWidget(create_card("Police Update", "12"))
        stats_layout.addWidget(create_card("Certificate Issued", "7"))
        stats_layout.addWidget(create_card("Pending Request", "14"))

        content_layout.addLayout(stats_layout)

        # Recent Activity (Scroll Area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        activity_widget = QWidget()
        activity_layout = QVBoxLayout(activity_widget)

        for i in range(10):
            activity_layout.addWidget(QLabel(f"Recent Activity {i+1}"))

        scroll.setWidget(activity_widget)
        content_layout.addWidget(scroll)

        # Quick Actions
        actions_layout = QHBoxLayout()

        for text in ["Add Resident", "Issue Certificate", "View Records"]:
            btn = QPushButton(text)
            btn.setStyleSheet("padding:10px;")
            actions_layout.addWidget(btn)

        content_layout.addLayout(actions_layout)

        # ===== ADD TO MAIN =====
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
