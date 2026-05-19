import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QStackedWidget, QHeaderView, QGroupBox, QScrollArea,
    QTabWidget, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from styles.theme import APP_STYLE, COLORS, SIDEBAR_STYLE
from database_conn import database


class StudentPortal(QMainWindow):
    def __init__(self, lrn, username):
        super().__init__()
        self.lrn = lrn
        self.username = username
        self.student_info = self._fetch_student_info()

        full_name = ""
        if self.student_info:
            fn = self.student_info.get('first_name', '')
            ln = self.student_info.get('last_name', '')
            full_name = f"{fn} {ln}".strip()

        self.setWindowTitle(f"Springfield Academy — Student Portal ({full_name or username})")
        self.setMinimumSize(1050, 650)
        self.setStyleSheet(APP_STYLE + SIDEBAR_STYLE)
        self._build_ui()

    def _fetch_student_info(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT si.*, ss.status, ss.feedback
                FROM student_info si
                JOIN student_status ss ON si.lrn_id = ss.student_lrn
                WHERE si.lrn_id = %s
            """, (self.lrn,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
        finally:
            cur.close()
            conn.close()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QHBoxLayout(central)
        main.setSpacing(0)
        main.setContentsMargins(0, 0, 0, 0)

        # ── Sidebar ──────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(12, 20, 12, 20)
        sb.setSpacing(4)

        fn = self.student_info.get('first_name', '') if self.student_info else ''
        ln = self.student_info.get('last_name', '') if self.student_info else ''
        full_name = f"{fn} {ln}".strip() or self.username

        school_lbl = QLabel("Springfield\nAcademy")
        school_lbl.setStyleSheet("color: white; font-size: 16px; font-weight: 800; padding: 8px 4px;")
        name_lbl = QLabel(f"👤 {full_name}")
        name_lbl.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 11px; padding: 0 4px 12px 4px;")
        name_lbl.setWordWrap(True)

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "🏠  My Dashboard"),
            ("schedule",  "📅  Class Schedule"),
            ("grades",    "📊  My Grades"),
            ("announcements", "📢  Announcements"),
        ]

        sb.addWidget(school_lbl)
        sb.addWidget(name_lbl)

        for key, label in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("nav_btn")
            btn.clicked.connect(lambda _, k=key: self._navigate(k))
            sb.addWidget(btn)
            self.nav_buttons[key] = btn

        sb.addStretch()
        logout_btn = QPushButton("🚪  Logout")
        logout_btn.setObjectName("logout_btn")
        logout_btn.clicked.connect(self._logout)
        sb.addWidget(logout_btn)

        # ── Content ──────────────────────────────────────────
        self.content_stack = QStackedWidget()
        self.dashboard_page = self._build_dashboard()
        self.schedule_page  = self._build_schedule()
        self.grades_page    = self._build_grades()
        self.ann_page       = self._build_announcements()

        for p in [self.dashboard_page, self.schedule_page, self.grades_page, self.ann_page]:
            self.content_stack.addWidget(p)

        self.page_index = {"dashboard": 0, "schedule": 1, "grades": 2, "announcements": 3}

        main.addWidget(sidebar)
        main.addWidget(self.content_stack, 1)

        self._navigate("dashboard")

    # ── Dashboard ─────────────────────────────────────────────
    def _build_dashboard(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        si = self.student_info or {}
        fn = si.get('first_name', self.username)
        ln = si.get('last_name', '')

        title = QLabel(f"Welcome, {fn} {ln} 👋")
        title.setObjectName("section_title")

        # Status card
        status = si.get('status', 'N/A')
        feedback = si.get('feedback', '')
        color = COLORS['warning'] if status == 'Pending' else COLORS['success'] if status == 'Approved' else COLORS['danger']

        status_card = QGroupBox("Enrollment Status")
        status_card.setStyleSheet(f"""
            QGroupBox {{
                background: white;
                border: none;
                border-left: 5px solid {color};
                border-radius: 8px;
                padding: 16px;
                font-weight: 700;
                color: {COLORS['primary']};
            }}
        """)
        sc_layout = QVBoxLayout(status_card)
        status_lbl = QLabel(f"Status: {status}")
        status_lbl.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {color};")
        sc_layout.addWidget(status_lbl)
        if feedback:
            fb_lbl = QLabel(f"Feedback: {feedback}")
            fb_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px;")
            fb_lbl.setWordWrap(True)
            sc_layout.addWidget(fb_lbl)

        # Info cards row
        info_row = QHBoxLayout()
        info_items = [
            ("LRN", si.get('lrn_id', '—')),
            ("Grade Level", si.get('grade_level', '—')),
            ("Strand", si.get('strand', '—')),
            ("School Year", si.get('school_year', '—')),
        ]
        for lbl, val in info_items:
            card = QGroupBox()
            card.setStyleSheet("QGroupBox { background: white; border: none; border-radius: 8px; padding: 14px; }")
            cl = QVBoxLayout(card)
            v = QLabel(val)
            v.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['primary']};")
            l = QLabel(lbl)
            l.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; font-weight: 600;")
            cl.addWidget(v)
            cl.addWidget(l)
            info_row.addWidget(card)

        layout.addWidget(title)
        layout.addWidget(status_card)
        layout.addLayout(info_row)
        layout.addStretch()
        return page

    # ── Schedule ──────────────────────────────────────────────
    def _build_schedule(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("Class Schedule")
        title.setObjectName("section_title")

        tabs = QTabWidget()
        self.sem1_table = self._schedule_table()
        self.sem2_table = self._schedule_table()
        tabs.addTab(self.sem1_table, "1st Semester")
        tabs.addTab(self.sem2_table, "2nd Semester")

        layout.addWidget(title)
        layout.addWidget(tabs)
        return page

    def _schedule_table(self):
        tbl = QTableWidget()
        tbl.setColumnCount(5)
        tbl.setHorizontalHeaderLabels(["Subject", "Teacher", "Day & Time", "Room", "Grade Level"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.verticalHeader().setVisible(False)
        tbl.setAlternatingRowColors(True)
        return tbl

    # ── Grades ────────────────────────────────────────────────
    def _build_grades(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("My Grades")
        title.setObjectName("section_title")

        tabs = QTabWidget()
        self.grades_sem1 = self._grades_table()
        self.grades_sem2 = self._grades_table()
        tabs.addTab(self.grades_sem1, "1st Semester")
        tabs.addTab(self.grades_sem2, "2nd Semester")

        layout.addWidget(title)
        layout.addWidget(tabs)
        return page

    def _grades_table(self):
        tbl = QTableWidget()
        tbl.setColumnCount(4)
        tbl.setHorizontalHeaderLabels(["Subject", "Grade", "School Year", "Remarks"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.verticalHeader().setVisible(False)
        tbl.setAlternatingRowColors(True)
        return tbl

    # ── Announcements ─────────────────────────────────────────
    def _build_announcements(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("Announcements")
        title.setObjectName("section_title")

        self.ann_table = QTableWidget()
        self.ann_table.setColumnCount(4)
        self.ann_table.setHorizontalHeaderLabels(["Title", "Target", "Posted By", "Date"])
        self.ann_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ann_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.ann_table.verticalHeader().setVisible(False)
        self.ann_table.setAlternatingRowColors(True)
        self.ann_table.cellClicked.connect(self._show_ann_content)

        self.ann_body = QTextEdit()
        self.ann_body.setReadOnly(True)
        self.ann_body.setMaximumHeight(150)
        self.ann_body.setPlaceholderText("Click an announcement to read it...")

        layout.addWidget(title)
        layout.addWidget(self.ann_table)
        layout.addWidget(self.ann_body)
        return page

    # ── Navigate ──────────────────────────────────────────────
    def _navigate(self, key):
        for k, btn in self.nav_buttons.items():
            btn.setObjectName("nav_btn_active" if k == key else "nav_btn")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self.content_stack.setCurrentIndex(self.page_index[key])

        if key == "schedule":
            self._load_schedule()
        elif key == "grades":
            self._load_grades()
        elif key == "announcements":
            self._load_announcements()

    # ── Data ──────────────────────────────────────────────────
    def _load_schedule(self):
        si = self.student_info or {}
        strand = si.get('strand', '')
        grade  = si.get('grade_level', '')

        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            for sem, tbl in [('1st', self.sem1_table), ('2nd', self.sem2_table)]:
                cur.execute("""
                    SELECT subject, teacher, day_time, room, grade_level
                    FROM class_schedule
                    WHERE strand=%s AND grade_level=%s AND semester=%s
                """, (strand, grade, sem))
                rows = cur.fetchall()
                tbl.setRowCount(len(rows))
                for r, row in enumerate(rows):
                    for c, val in enumerate(row):
                        tbl.setItem(r, c, QTableWidgetItem(str(val)))
        finally:
            cur.close()
            conn.close()

    def _load_grades(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            for sem, tbl in [('1st', self.grades_sem1), ('2nd', self.grades_sem2)]:
                cur.execute("""
                    SELECT subject, grade, school_year FROM student_grades
                    WHERE student_lrn=%s AND semester=%s
                """, (self.lrn, sem))
                rows = cur.fetchall()
                tbl.setRowCount(len(rows))
                for r, row in enumerate(rows):
                    subject, grade, sy = row
                    tbl.setItem(r, 0, QTableWidgetItem(subject))
                    grade_item = QTableWidgetItem(str(grade))
                    if grade is not None:
                        if float(grade) >= 75:
                            grade_item.setForeground(QColor(COLORS['success']))
                        else:
                            grade_item.setForeground(QColor(COLORS['danger']))
                    tbl.setItem(r, 1, grade_item)
                    tbl.setItem(r, 2, QTableWidgetItem(str(sy)))
                    remarks = "Passed" if grade is not None and float(grade) >= 75 else "Failed" if grade else "—"
                    tbl.setItem(r, 3, QTableWidgetItem(remarks))
        finally:
            cur.close()
            conn.close()

    def _load_announcements(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, title, target, posted_by, DATE_FORMAT(created_at,'%Y-%m-%d %H:%i'), content
                FROM announcements
                WHERE target IN ('student', 'both')
                ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        self.ann_table.setRowCount(len(rows))
        self._ann_data = {}
        for r, row in enumerate(rows):
            ann_id, title, target, posted_by, dt, content = row
            self._ann_data[r] = content
            for c, val in enumerate([title, target, posted_by, dt]):
                self.ann_table.setItem(r, c, QTableWidgetItem(str(val)))

    def _show_ann_content(self, row, col):
        self.ann_body.setPlainText(self._ann_data.get(row, ""))

    def _logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            from views.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
