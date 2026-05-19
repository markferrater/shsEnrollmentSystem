# pip install matplotlib
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QLabel, QHBoxLayout, QScrollArea, QSizePolicy, QLineEdit, QGroupBox, QDateEdit, QComboBox)


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

        # Studentbtn.clicked.connect(self.showStudent)
        # Staffbtn.clicked.connect(self.showStaff)

        header_child.addWidget(Studentbtn)
        header_child.addWidget(Staffbtn)

        main_layout.addWidget(header_cardT)
        main_layout.addWidget(header_child_widget)

        # ----- BODY -----
        self.header_cardB = QWidget()
        self.header_cardB.setStyleSheet("""
            background: white;
            color:white;
            padding:15px;
            border-radius:15px;
        """)
        # IMPORTANT: Make it expand to fill space
        self.header_cardB.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create horizontal layout for left and right panels
        self.body_layout = QHBoxLayout(self.header_cardB)
        main_layout.addWidget(self.header_cardB, 1)

        # Create MAIN GROUP BOX with SCROLL AREA
        main_group = QGroupBox("Student Form")
        main_group.setStyleSheet("""
        background: #f1f1f1;
        border: 1px solid gray;
        margin: 2px;
        color: gray;
        """)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background: #f1f1f1;
        }
        QScrollBar:vertical {
            border: none;
            background: #f1f1f1;
            width: 10px;
            margin: 0px;
        }
     
        """)

        # Create content widget for scroll area
        scroll_content = QWidget()
        scroll_content.setObjectName('scroll_content')
        scroll_content.setStyleSheet("""
        QWidget{
        background: #f1f1f1; 
        }
        
        QWidget#scroll_content{
        border: none;
        }
        """)
        scroll_layout = QVBoxLayout(scroll_content)

        # Add group boxes to scroll layout
        personal_info = QGroupBox('Personal Information')
        personal_info_layout = QVBoxLayout(personal_info)

        personal_info_layoutH1 = QHBoxLayout()
        personal_info_layoutH2 = QHBoxLayout()

        personal_info_layout.addLayout(personal_info_layoutH1)
        personal_info_layout.addLayout(personal_info_layoutH2)

        first_name = QLineEdit()
        first_name.setPlaceholderText('First Name')
        first_name.setStyleSheet("""
        border: 1px solid gray;
        border-radius: 6px;
        padding: 3px;
        """)

        middle_name = QLineEdit()
        middle_name.setPlaceholderText('Middle Name')
        middle_name.setStyleSheet("""
                border: 1px solid gray;
                border-radius: 6px;
                padding: 3px;
                """)

        last_name = QLineEdit()
        last_name.setPlaceholderText('Last Name')
        last_name.setStyleSheet("""
                border: 1px solid gray;
                border-radius: 6px;
                padding: 3px;
                """)

        date_of_birth = QDateEdit()
        date_of_birth.setDisplayFormat("MMM d, yyyy")
        date_of_birth.setStyleSheet("""
        QDateEdit {
        border: 1px solid gray;
        border-radius: 6px;
        padding: 3px;
        }

        QDateEdit:focus {
        outline: none; 
        }
        """)
        date_of_birth.setCalendarPopup(True)

        gender = QComboBox()
        gender.setPlaceholderText('Select your Gender')
        gender.addItems(["Male", "Female"])
        gender.setStyleSheet("""
        border: 1px solid gray;
        border-radius: 6px;
        padding: 3px;
        """)

        personal_info_layoutH1.addWidget(first_name)
        personal_info_layoutH1.addWidget(middle_name)
        personal_info_layoutH1.addWidget(last_name)

        personal_info_layoutH2.addWidget(date_of_birth)
        personal_info_layoutH2.addWidget(gender)

        contact_info = QGroupBox('Contact Information')
        contact_info_layout = QVBoxLayout(contact_info)
        contact_info.setStyleSheet("""
        padding: 0px;
        padding-top: 4px;
        padding-bottom: 4px;
        margin: 0 ;
        """)

        email_gbox = QGroupBox('Email Address')
        email_gbox.setObjectName("test")
        email_gbox.setStyleSheet("""
        QGroupBox#test {
        border: none;
        margin-top: 10px;
        margin-left: 10px;
        margin-right: 10px;
        padding-top: 9px; 
        border-radius: 9px;
        }

        QLineEdit#email_test {
        border: 1px solid gray;
        padding: 3px;
        border-radius: 7px;
        }
        """)
        email_gbox_layout = QVBoxLayout(email_gbox)
        email_input = QLineEdit()
        email_input.setPlaceholderText("Enter your email address")
        email_input.setObjectName("email_test")

        # ==========================================================

        phone_gbox = QGroupBox("Phone Number")
        phone_gbox_layout = QVBoxLayout(phone_gbox)
        phone_gbox.setObjectName("phone_gbox")

        phone_input = QLineEdit()
        phone_input.setPlaceholderText("Ex: 0992761184")
        phone_input.setObjectName("phone_input")

        phone_gbox.setStyleSheet("""
                QGroupBox#phone_gbox {
                border: none;
                margin-left: 10px;
                margin-right: 10px;   
                padding-top: 10px;
                border-radius: 9px;
                }

                QLineEdit#phone_input {
                border: 1px solid gray;
                padding: 3px;
                border-radius: 7px;
                }
                """)

        email_gbox_layout.addWidget(email_input)
        phone_gbox_layout.addWidget(phone_input)

        email_gbox_layout.setContentsMargins(9, 10, 0, 0)
        phone_gbox_layout.setContentsMargins(9, 10, 0, 0)

        contact_info_layout.addWidget(email_gbox)
        contact_info_layout.addWidget(phone_gbox)

        guardian_info = QGroupBox('Guardian Information')
        guardian_info.setObjectName('guardian_info')

        guardian_info.setStyleSheet("""
        #guardian_info{
          padding: 6px;
          padding-top: 9px;
          
        }
        
        #guardian_first_name_gbox_input, #guardian_middle_name_gbox_input, #guardian_last_name_gbox_input, #guardian_phone_gbox_input, #guardian_current_rel_input{
                   margin: 0px;
                   margin-top: 5px;
                   border-radius: 7px;
                   width: 30px;
                   padding: 3px;
                
                }
                
                #guardian_first_name_gbox, #guardian_middle_name_gbox, #guardian_last_name_gbox, #guardian_phone_gbox, #guardian_current_rel_gbox{
                margin:0px;
                padding: 0px; 
                margin-left: 1px;
               
                }
        """)

        guardian_info_layout_main = QVBoxLayout(guardian_info)
        guardian_info_layoutT = QHBoxLayout()
        guardian_info_layoutT.setSpacing(0)

        guardian_info_layoutB = QHBoxLayout()

        # ==========Top content =============
        guardian_first_name_gbox = QGroupBox('First name')
        guardian_first_name_gbox.setFixedHeight(60)
        guardian_first_name_gbox.setObjectName("guardian_first_name_gbox")

        guardian_middle_name_gbox = QGroupBox('Middle name')
        guardian_middle_name_gbox.setFixedHeight(60)
        guardian_middle_name_gbox.setObjectName("guardian_middle_name_gbox")

        guardian_last_name_gbox = QGroupBox('Last name')
        guardian_last_name_gbox.setFixedHeight(60)
        guardian_last_name_gbox.setObjectName("guardian_last_name_gbox")

        guardian_first_name_gbox_layout = QVBoxLayout(guardian_first_name_gbox)
        guardian_middle_name_gbox_layout = QVBoxLayout(guardian_middle_name_gbox)
        guardian_last_name_gbox_layout = QVBoxLayout(guardian_last_name_gbox)

        guardian_first_name_gbox_input = QLineEdit()
        guardian_first_name_gbox_input.setFixedHeight(30)
        guardian_first_name_gbox_input.setObjectName("guardian_first_name_gbox_input")

        guardian_middle_name_gbox_input = QLineEdit()
        guardian_middle_name_gbox_input.setFixedHeight(30)
        guardian_middle_name_gbox_input.setObjectName("guardian_middle_name_gbox_input")

        guardian_last_name_gbox_input = QLineEdit()
        guardian_last_name_gbox_input.setFixedHeight(30)
        guardian_last_name_gbox_input.setObjectName("guardian_last_name_gbox_input")

        guardian_first_name_gbox_layout.addWidget(guardian_first_name_gbox_input)
        guardian_middle_name_gbox_layout.addWidget(guardian_middle_name_gbox_input)
        guardian_last_name_gbox_layout.addWidget(guardian_last_name_gbox_input)


        guardian_info_layoutT.addWidget(guardian_first_name_gbox)
        guardian_info_layoutT.addWidget(guardian_middle_name_gbox)
        guardian_info_layoutT.addWidget(guardian_last_name_gbox)

        # ==========Bottom content =============
        guardian_phone_gbox = QGroupBox('Guardians phone number')
        guardian_phone_gbox.setObjectName('guardian_phone_gbox')

        guardian_current_rel_gbox = QGroupBox('Current relationship')
        guardian_current_rel_gbox.setObjectName('guardian_current_rel_gbox')

        guardian_phone_gbox_layout = QVBoxLayout(guardian_phone_gbox)
        guardian_current_rel_gbox_layout = QVBoxLayout(guardian_current_rel_gbox)

        guardian_phone_gbox_input = QLineEdit()
        guardian_phone_gbox_input.setObjectName("guardian_phone_gbox_input")
        guardian_phone_gbox_input.setFixedHeight(30)

        guardian_current_rel_input = QLineEdit()
        guardian_current_rel_input.setObjectName("guardian_current_rel_input")
        guardian_current_rel_input.setFixedHeight(30)

        guardian_phone_gbox_layout.addWidget(guardian_phone_gbox_input)
        guardian_current_rel_gbox_layout.addWidget(guardian_current_rel_input)


        guardian_info_layoutB.addWidget(guardian_phone_gbox)
        guardian_info_layoutB.addWidget(guardian_current_rel_gbox)

        guardian_info_layout_main.addLayout(guardian_info_layoutT)
        guardian_info_layout_main.addLayout(guardian_info_layoutB)


        #=======================main_groupbox=========================
        academic_info = QGroupBox('Academic Information')
        academic_info.setObjectName('academic_info')
        academic_info.setStyleSheet("""
                #academic_info{
                  padding: 6px;
                  padding-top: 90px;
          
                 }
        
                #academic_grade_level_input, #academic_strand_input, #academic_semester_input, #academic_previous_school_input, #academic_school_year_input{
                   margin: 0px;
                   margin-top: 5px;
                   border-radius: 4px;
                   width: 30px;
                   padding: 3px;
                
                }
                
                #academic_grade_level,#academic_strand, #academic_semester, #academic_previous_school, #academic_school_year{
                margin:0px;
                padding: 0px; 
                margin-left: 1px;
                
                }
                """)
        academic_info.setObjectName('Academic Information')
        academic_info_layout = QHBoxLayout(academic_info)
        academic_info_layout.setSpacing(0)


        # =======================inner_child_groupbox=========================
        academic_grade_level = QGroupBox('Grade level')
        academic_grade_level.setFixedHeight(60)
        academic_grade_level.setObjectName('academic_grade_level')

        academic_strand = QGroupBox('Strand')
        academic_strand.setFixedHeight(60)
        academic_strand.setObjectName('academic_strand')

        academic_semester = QGroupBox('Semester')
        academic_semester.setFixedHeight(60)
        academic_semester.setObjectName('academic_semester')

        academic_previous_school = QGroupBox('Previous school')
        academic_previous_school.setFixedHeight(60)
        academic_previous_school.setObjectName('academic_previous_school')

        academic_school_year = QGroupBox('School year')
        academic_school_year.setFixedHeight(60)
        academic_school_year.setObjectName('academic_school_year')

        # =======================inner_child_groupbox_layout=========================
        academic_grade_level_layout = QVBoxLayout(academic_grade_level)
        academic_strand_layout = QVBoxLayout(academic_strand)
        academic_semester_layout = QVBoxLayout(academic_semester)
        academic_previous_school_layout = QVBoxLayout(academic_previous_school)
        academic_school_year_layout = QVBoxLayout(academic_school_year)

        # =======================inner_child_groupbox_input=============
        academic_grade_level_input = QLineEdit()
        academic_grade_level_input.setFixedHeight(30)
        academic_grade_level_input.setObjectName('academic_grade_level_input')

        academic_strand_input  = QLineEdit()
        academic_strand_input.setFixedHeight(30)
        academic_strand_input.setObjectName('academic_strand_input')

        academic_semester_input  = QLineEdit()
        academic_semester_input.setFixedHeight(30)
        academic_semester_input.setObjectName('academic_semester_input')

        academic_previous_school_input  = QLineEdit()
        academic_previous_school_input.setFixedHeight(30)
        academic_previous_school_input.setObjectName('academic_previous_school_input')

        academic_school_year_input  = QLineEdit()
        academic_school_year_input.setFixedHeight(30)
        academic_school_year_input.setObjectName('academic_school_year_input')

        # =======================adding input to the main layout=============
        academic_grade_level_layout.addWidget(academic_grade_level_input)
        academic_strand_layout.addWidget(academic_strand_input)
        academic_semester_layout.addWidget(academic_semester_input)
        academic_previous_school_layout.addWidget(academic_previous_school_input)
        academic_school_year_layout.addWidget(academic_school_year_input)

        # =======================adding inner_child_groupbox from the main_layout=========================
        academic_info_layout.addWidget(academic_grade_level)
        academic_info_layout.addWidget(academic_strand)
        academic_info_layout.addWidget(academic_semester)
        academic_info_layout.addWidget(academic_previous_school)
        academic_info_layout.addWidget(academic_school_year)

        Submit_btn = QPushButton('Submit')
        Submit_btn.setStyleSheet("""
        QPushButton {
        padding: 3px;
        border-radius: 8px;
        background-color: black;
        color: white;
        }     

        QPushButton:hover{
        background: grey;
        color: ;
        }

        QPushButton:pressed{
        background: white;
        color: black;
        }

        """)

        # Add widgets to scroll layout
        scroll_layout.addWidget(personal_info)
        scroll_layout.addWidget(contact_info)
        scroll_layout.addWidget(guardian_info)
        scroll_layout.addWidget(academic_info)
        scroll_layout.addWidget(Submit_btn)
        scroll_layout.addStretch()

        # Set up scroll area
        scroll_area.setWidget(scroll_content)

        # Create layout for main_group and add scroll area
        main_group_layout = QVBoxLayout(main_group)
        main_group_layout.addWidget(scroll_area)

        self.body_layout.addWidget(main_group)

        self.showMaximized()


if __name__ == '__main__':
    app = QApplication([])
    w = Dashboard()
    w.show()
    sys.exit(app.exec())