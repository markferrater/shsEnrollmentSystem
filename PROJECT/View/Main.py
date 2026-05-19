# pip install matplotlib
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QLabel, QHBoxLayout, QScrollArea, QSizePolicy, QLineEdit)


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dashboard')

        self.setStyleSheet("background:#f2fafc;")
        self.setWindowIcon(QIcon("../../FInal_Project/View/Logo.png"))

        # ==================Logo==================
        logo = QLabel()
        pixmap = QPixmap("../../FInal_Project/View/Logo.png")
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        logo.setFixedSize(150, 150)

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        log_outbtn = QPushButton("Log Out")
        log_outbtn.setStyleSheet("""
        QPushButton {
            background:#f72d2d;
            font-weight:bold;
            border-radius:15px;
            padding:8px 15px;
        }
        QPushButton:hover {
            background: #bd3e3e;
            color:white;
        }
        QPushButton:pressed {
            background: #fa8787;
            color: #363433;
        }
        """)

        # ==================Main layout==================
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # ----- HEADER -----
        header_layout = QHBoxLayout()
        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(log_outbtn)

        header_cardT = QWidget()
        header_cardT.setStyleSheet("""
         background:#444;
         color:white;
         padding:20px;
         border-radius:15px;
        """)
        header_cardT.setFixedHeight(120)
        header_cardT.setLayout(header_layout)

        header_child_widget = QWidget()
        header_child_widget.setStyleSheet("""
        background:#635b5a;
        color:white;
        """)
        header_child = QHBoxLayout(header_child_widget)
        Studentbtn = QPushButton('student btn')
        Staffbtn = QPushButton('staff btn')

        Studentbtn.clicked.connect(self.showStudent)
        Staffbtn.clicked.connect(self.showStaff)

        # Store the student form as an instance variable
        self.student_form = studentForm()

        # Store the dashboard content as an instance variable
        self.dashboard_content = None

        header_child.addWidget(Studentbtn)
        header_child.addWidget(Staffbtn)

        main_layout.addWidget(header_cardT)
        main_layout.addWidget(header_child_widget)

        # ----- BODY CONTAINER (This will be swapped) -----
        self.header_cardB = QWidget()
        self.header_cardB.setStyleSheet("""
            background:#635b5a;
            color:white;
            padding:15px;
            border-radius:15px;
        """)
        self.header_cardB.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.header_cardB, 1)

        # Create and store the dashboard content
        self.createDashboardContent()

        # Show dashboard by default
        self.showDashboard()

        self.showMaximized()

    def createDashboardContent(self):
        """Create the dashboard content and store it"""
        # Create a widget to hold the dashboard content
        self.dashboard_content = QWidget()

        # Create horizontal layout for left and right panels
        body_layout = QHBoxLayout(self.dashboard_content)

        # ===== LEFT PANEL (Scrollable student cards) =====
        left_widget = QWidget()
        left_widget.setStyleSheet("""
                            background: white;
                            color:black;
                            padding:15px;
                            border-radius:15px;
                        """)
        left_content = QVBoxLayout(left_widget)

        search_header = QHBoxLayout()
        content_body = QVBoxLayout()

        left_content.addLayout(search_header)
        left_content.addLayout(content_body)

        search_label = QLabel('Search: 🔎')
        search_label.setStyleSheet("""
        margin: 1px;
        """)

        search = QLineEdit()
        search.setPlaceholderText('Search by id or name')
        search.setStyleSheet("""
        border: 1px solid;
        padding: 7px;
        margin-right: 20px;
        border-radius: 10px;
        color:black;
        """)

        search_button = QPushButton('search')
        search_button.setStyleSheet("""
        QPushButton{
         border-radius: 5px;
         border: 1px solid grey;
         width: 55px;
         padding: 8px;
         margin-right: 20px;
        }

        QPushButton:hover{
        background-color: black;
        color: white;
        }

        QPushButton:pressed{
        background-color: grey;
        color: white;
        }

        """)

        search_header.addWidget(search_label)
        search_header.addWidget(search)
        search_header.addWidget(search_button)

        # ======Content body=================
        student_widget = QWidget()
        student_widget.setStyleSheet("""
                    background:grey;
                    color:white;
                    padding:15px;
                    border-radius:15px;
                """)
        student_layout = QVBoxLayout(student_widget)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Widget inside scroll area
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # STUDENT DATA
        self.students = [
            {"id": 1001, "name": "Mark", "course": "Computer Science"},
            {"id": 1002, "name": "John", "course": "Engineering"},
            {"id": 1003, "name": "Albert", "course": "Mathematics"},
            {"id": 1004, "name": "Peter", "course": "Physics"},
            {"id": 1005, "name": "Sarah", "course": "Biology"},
            {"id": 1006, "name": "Mike", "course": "Chemistry"},
            {"id": 1007, "name": "Emma", "course": "Literature"},
            {"id": 1008, "name": "David", "course": "History"},
            {"id": 1009, "name": "Lisa", "course": "Art"},
            {"id": 1010, "name": "James", "course": "Music"},
        ]

        for i, student in enumerate(self.students):
            student_id = student["id"]
            student_name = student["name"]
            student_course = student["course"]

            label_input = f"ID: {student_id}\nName: {student_name}\nCourse: {student_course}"

            # Create card for each student
            card_row = QWidget()
            card_row.setStyleSheet("""
                           QWidget {
                               background-color: white;
                               border: 2px solid #e0e0e0;
                               border-radius: 12px;
                               margin: 8px;
                               padding: 12px;
                           }
                           QWidget:hover {
                               border-color: #007bff;
                               background-color: #f8f9fa;
                           }
                       """)
            card_row_layout = QHBoxLayout(card_row)

            # Student info label
            label = QLabel(label_input)
            label.setStyleSheet("""
                            QLabel {
                                color: black;
                                font-weight: bold;
                                font-size: 14px;
                                padding: 5px;
                                border: none;
                            }
                        """)
            card_row_layout.addWidget(label, 2)

            # Button
            button = QPushButton(f'View Details')
            button.clicked.connect(lambda checked, index=i: self.clicked(index))
            button.setStyleSheet("""
                            QPushButton {
                                border: 1px solid #007bff;
                                background-color: white;
                                color: #007bff;
                                padding: 8px 15px;
                                border-radius: 5px;
                                font-weight: bold;
                                min-width: 100px;
                            }
                            QPushButton:hover {
                                background-color: #007bff;
                                color: white;
                            }
                        """)
            card_row_layout.addWidget(button)

            scroll_layout.addWidget(card_row)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)

        student_layout.addWidget(scroll_area)

        content_body.addWidget(student_widget)

        # ===== Right PANEL =====
        right_widget = QWidget()
        right_widget.setStyleSheet("""
                            background: white;
                            color:black;
                            padding:15px;
                            border-radius:15px;
                        """)

        right_layout = QVBoxLayout(right_widget)

        view_layout = QVBoxLayout()

        l1 = QLabel('Student Details')
        l1.setStyleSheet("""
        font-size:18px; 
        font-weight:bold;
        """)

        self.l2 = QWidget()
        self.l2.setStyleSheet("""        
        """)
        self.l2_layout = QVBoxLayout(self.l2)

        self.showDefault()

        view_layout.addWidget(l1)
        view_layout.addWidget(self.l2, 2)

        right_layout.addLayout(view_layout)
        body_layout.addWidget(left_widget, 1)
        body_layout.addWidget(right_widget, 1)

    def clicked(self, num):
        student = self.students[num]

        # data for students
        student_id = student["id"]
        student_name = student["name"]
        student_course = student["course"]

        self.clear_container()

        info_widget = QWidget()
        info_widget.setStyleSheet("""
          QWidget{
            border: 1px solid grey;
            border-radius: 9px;
          }

          QLabel {
           font: Segoe UI ;
           border: none;
          }

        """)
        info_layout = QVBoxLayout(info_widget)

        main_header = QHBoxLayout()
        header = QVBoxLayout()
        Ttest1 = QLabel(f'Name: <b>{student_name}</b>')
        Ttest2 = QLabel(f'ID: <b>{student_id}</b>')

        header.addWidget(Ttest1)
        header.addWidget(Ttest2)
        main_header.addLayout(header)

        main_bottom = QHBoxLayout()

        bottom = QVBoxLayout()
        test1 = QLabel('Date of birth: ')
        test2 = QLabel('Email: ')
        test3 = QLabel('Guardian:')
        test4 = QLabel('Semester: ')

        bottom.addWidget(test1)
        bottom.addWidget(test2)
        bottom.addWidget(test3)
        bottom.addWidget(test4)

        bottom_child = QVBoxLayout()
        Stest1 = QLabel('Gender: ')
        Stest2 = QLabel('Contact Number: ')
        Stest3 = QLabel(f'Strand: <b>{student_course}</b>')
        Stest4 = QLabel('School year')

        bottom_child.addWidget(Stest1)
        bottom_child.addWidget(Stest2)
        bottom_child.addWidget(Stest3)
        bottom_child.addWidget(Stest4)

        main_bottom.addLayout(bottom)
        main_bottom.addLayout(bottom_child)

        info_layout.addLayout(main_header)
        info_layout.addLayout(main_bottom)

        self.l2_layout.addWidget(info_widget)

    def showDefault(self):
        default_label = QLabel('Select a student to view details')
        default_label.setStyleSheet("""
                    font-size: 16px; 
                    color: #7f8c8d;
                    padding: 50px;
                """)
        default_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l2_layout.addWidget(default_label)

    def clear_container(self):
        while self.l2_layout.count():
            item = self.l2_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def setBodyContent(self, content_widget):
        """Replace the content in the body container"""
        # Clear existing layout
        if self.header_cardB.layout():
            old_layout = self.header_cardB.layout()
            # Remove all widgets from the layout
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            # Delete the old layout
            old_layout.deleteLater()

        # Create new layout and add the content widget
        new_layout = QVBoxLayout(self.header_cardB)
        new_layout.addWidget(content_widget)

    def showDashboard(self):
        """Show the dashboard content"""
        if self.dashboard_content:
            self.setBodyContent(self.dashboard_content)

    def showStudent(self):
        """Show the student form"""
        self.setBodyContent(self.student_form)

    def showStaff(self):
        """Show the dashboard (for now)"""
        self.showDashboard()


class studentForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #ff6b6b;")
        layout = QVBoxLayout(self)

        label = QLabel("I am the RED widget (Student Form)")
        label.setStyleSheet("color: white; font-size: 20px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add a back button to return to dashboard
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #ff6b6b;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        back_btn.clicked.connect(self.goBack)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def goBack(self):
        """Find parent Dashboard and switch back"""
        parent = self.parent()
        while parent and not isinstance(parent, Dashboard):
            parent = parent.parent()
        if parent:
            parent.showDashboard()


if __name__ == '__main__':
    app = QApplication([])
    w = Dashboard()
    w.show()
    sys.exit(app.exec())