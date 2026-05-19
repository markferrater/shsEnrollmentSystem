import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QMessageBox, QDialog, QDialogButtonBox, QLineEdit, QStackedWidget,
    QHeaderView, QSplitter, QGroupBox, QScrollArea, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from styles.theme import APP_STYLE, COLORS, SIDEBAR_STYLE
from database_conn import database


class FeedbackDialog(QDialog):
    def __init__(self, student_name, action, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{action} Student")
        self.setMinimumWidth(420)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(f"{action}: {student_name}")
        title.setStyleSheet(f"font-size: 15px; font-weight: 700; color: {COLORS['primary']};")

        lbl = QLabel("Feedback message to student (required):")
        self.feedback_box = QTextEdit()
        self.feedback_box.setPlaceholderText("Write your feedback or reason here...")
        self.feedback_box.setMinimumHeight(100)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._accept)
        btns.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(lbl)
        layout.addWidget(self.feedback_box)
        layout.addWidget(btns)

    def _accept(self):
        if not self.feedback_box.toPlainText().strip():
            QMessageBox.warning(self, "Required", "Please provide feedback.")
            return
        self.accept()

    def get_feedback(self):
        return self.feedback_box.toPlainText().strip()


class StaffPortal(QMainWindow):
    def __init__(self, staff_info, username):
        super().__init__()
        self.staff_info = staff_info  # (id, full_name)
        self.username = username
        self.staff_name = staff_info[1] if staff_info else username

        self.setWindowTitle(f"Springfield Academy — Staff Portal ({self.staff_name})")
        self.setMinimumSize(1100, 680)
        self.setStyleSheet(APP_STYLE + SIDEBAR_STYLE)

        self._build_ui()
        self._load_students()

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
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(12, 20, 12, 20)
        sb_layout.setSpacing(4)

        school_lbl = QLabel("Springfield\nAcademy")
        school_lbl.setStyleSheet("color: white; font-size: 16px; font-weight: 800; padding: 8px 4px;")
        staff_lbl = QLabel(f"👤 {self.staff_name}")
        staff_lbl.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 11px; padding: 0 4px 12px 4px;")
        staff_lbl.setWordWrap(True)

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "🏠  Dashboard"),
            ("applications", "📋  Student Applications"),
            ("approved", "✅  Approved Students"),
            ("announcements", "📢  Announcements"),
        ]

        sb_layout.addWidget(school_lbl)
        sb_layout.addWidget(staff_lbl)

        for key, label in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("nav_btn")
            btn.clicked.connect(lambda _, k=key: self._navigate(k))
            sb_layout.addWidget(btn)
            self.nav_buttons[key] = btn

        sb_layout.addStretch()
        logout_btn = QPushButton("🚪  Logout")
        logout_btn.setObjectName("logout_btn")
        logout_btn.clicked.connect(self._logout)
        sb_layout.addWidget(logout_btn)

        # ── Content area ─────────────────────────────────────
        self.content_stack = QStackedWidget()

        self.dashboard_page  = self._build_dashboard()
        self.applications_page = self._build_applications()
        self.approved_page   = self._build_approved()
        self.announcements_page = self._build_announcements()

        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.applications_page)
        self.content_stack.addWidget(self.approved_page)
        self.content_stack.addWidget(self.announcements_page)

        self.page_index = {
            "dashboard": 0, "applications": 1, "approved": 2, "announcements": 3
        }

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

        title = QLabel(f"Welcome, {self.staff_name} 👋")
        title.setObjectName("section_title")

        cards_row = QHBoxLayout()
        self.card_pending  = self._stat_card("Pending", "0", COLORS['warning'])
        self.card_approved = self._stat_card("Approved", "0", COLORS['success'])
        self.card_declined = self._stat_card("Declined", "0", COLORS['danger'])
        cards_row.addWidget(self.card_pending)
        cards_row.addWidget(self.card_approved)
        cards_row.addWidget(self.card_declined)

        layout.addWidget(title)
        layout.addLayout(cards_row)
        layout.addStretch()
        return page

    def _stat_card(self, label, value, color):
        card = QGroupBox()
        card.setStyleSheet(f"""
            QGroupBox {{
                background: white;
                border: none;
                border-left: 5px solid {color};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        layout = QVBoxLayout(card)
        val_lbl = QLabel(value)
        val_lbl.setStyleSheet(f"font-size: 36px; font-weight: 800; color: {color};")
        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']}; font-weight: 600;")
        layout.addWidget(val_lbl)
        layout.addWidget(lbl)
        card._value_label = val_lbl
        return card

    # ── Applications ──────────────────────────────────────────
    def _build_applications(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("Student Applications")
        title.setObjectName("section_title")
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._load_students)
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(refresh_btn)

        # Filter row
        filter_row = QHBoxLayout()
        self.filter_status = QPushButton("Pending")
        self.filter_all    = QPushButton("All")
        for btn in [self.filter_status, self.filter_all]:
            btn.setObjectName("outline_btn")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {COLORS['secondary']};
                    border: 1.5px solid {COLORS['secondary']};
                    border-radius: 5px;
                    padding: 5px 14px;
                    font-size: 12px;
                    font-weight: 600;
                    min-height: 28px;
                }}
                QPushButton:hover {{
                    background: {COLORS['secondary']};
                    color: white;
                }}
            """)
        self.filter_status.clicked.connect(lambda: self._load_students('Pending'))
        self.filter_all.clicked.connect(lambda: self._load_students())
        filter_row.addWidget(QLabel("Filter:"))
        filter_row.addWidget(self.filter_status)
        filter_row.addWidget(self.filter_all)
        filter_row.addStretch()

        self.apps_table = QTableWidget()
        self.apps_table.setColumnCount(8)
        self.apps_table.setHorizontalHeaderLabels([
            "LRN", "Full Name", "Grade", "Strand", "Email", "School Year", "Status", "Actions"
        ])
        self.apps_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.apps_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.apps_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.apps_table.verticalHeader().setVisible(False)
        self.apps_table.setAlternatingRowColors(True)

        layout.addLayout(hdr)
        layout.addLayout(filter_row)
        layout.addWidget(self.apps_table)
        return page

    # ── Approved ──────────────────────────────────────────────
    def _build_approved(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("Approved Students")
        title.setObjectName("section_title")

        self.approved_table = QTableWidget()
        self.approved_table.setColumnCount(6)
        self.approved_table.setHorizontalHeaderLabels(["LRN", "Full Name", "Grade", "Strand", "Email", "School Year"])
        self.approved_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.approved_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.approved_table.verticalHeader().setVisible(False)
        self.approved_table.setAlternatingRowColors(True)

        layout.addWidget(title)
        layout.addWidget(self.approved_table)
        return page

    # ── Announcements ─────────────────────────────────────────
    def _build_announcements(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("Announcements")
        title.setObjectName("section_title")

        self.staff_ann_list = QTableWidget()
        self.staff_ann_list.setColumnCount(4)
        self.staff_ann_list.setHorizontalHeaderLabels(["Title", "Target", "Posted By", "Date"])
        self.staff_ann_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.staff_ann_list.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.staff_ann_list.verticalHeader().setVisible(False)
        self.staff_ann_list.setAlternatingRowColors(True)
        self.staff_ann_list.cellClicked.connect(self._view_announcement)

        layout.addWidget(title)
        layout.addWidget(QLabel("Click an announcement to view full content."))
        layout.addWidget(self.staff_ann_list)

        self.ann_content = QTextEdit()
        self.ann_content.setReadOnly(True)
        self.ann_content.setMaximumHeight(150)
        self.ann_content.setPlaceholderText("Select an announcement to read it here...")
        layout.addWidget(self.ann_content)

        return page

    # ── Navigate ──────────────────────────────────────────────
    def _navigate(self, key):
        for k, btn in self.nav_buttons.items():
            btn.setObjectName("nav_btn_active" if k == key else "nav_btn")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self.content_stack.setCurrentIndex(self.page_index[key])

        if key == "dashboard":
            self._refresh_dashboard()
        elif key == "applications":
            self._load_students()
        elif key == "approved":
            self._load_approved()
        elif key == "announcements":
            self._load_announcements()

    # ── Data Loading ──────────────────────────────────────────
    def _load_students(self, status_filter=None):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            if status_filter:
                cur.execute("""
                    SELECT si.lrn_id, si.first_name, si.middle_name, si.last_name,
                           si.grade_level, si.strand, si.email, si.school_year, ss.status
                    FROM student_info si
                    JOIN student_status ss ON si.lrn_id = ss.student_lrn
                    WHERE ss.status = %s
                    ORDER BY si.registered_at DESC
                """, (status_filter,))
            else:
                cur.execute("""
                    SELECT si.lrn_id, si.first_name, si.middle_name, si.last_name,
                           si.grade_level, si.strand, si.email, si.school_year, ss.status
                    FROM student_info si
                    JOIN student_status ss ON si.lrn_id = ss.student_lrn
                    ORDER BY si.registered_at DESC
                """)
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        self.apps_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            lrn, fn, mn, ln, grade, strand, email, sy, status = row
            full_name = f"{fn} {mn or ''} {ln}".strip()
            items = [lrn, full_name, grade, strand, email, sy, status]
            for c, val in enumerate(items):
                item = QTableWidgetItem(str(val))
                if status == 'Pending':
                    item.setForeground(QColor(COLORS['warning']))
                elif status == 'Approved':
                    item.setForeground(QColor(COLORS['success']))
                elif status == 'Declined':
                    item.setForeground(QColor(COLORS['danger']))
                self.apps_table.setItem(r, c, item)

            # Actions cell
            if status == 'Pending':
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(4, 2, 4, 2)
                action_layout.setSpacing(6)

                approve_btn = QPushButton("✓ Approve")
                approve_btn.setObjectName("success_btn")
                approve_btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {COLORS['success']};
                        color: white;
                        border-radius: 4px;
                        padding: 4px 10px;
                        font-size: 11px;
                        font-weight: 700;
                        min-height: 26px;
                    }}
                    QPushButton:hover {{ background: #1E8449; }}
                """)
                approve_btn.clicked.connect(lambda _, lrn=lrn, name=full_name: self._approve_student(lrn, name))

                decline_btn = QPushButton("✗ Decline")
                decline_btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {COLORS['danger']};
                        color: white;
                        border-radius: 4px;
                        padding: 4px 10px;
                        font-size: 11px;
                        font-weight: 700;
                        min-height: 26px;
                    }}
                    QPushButton:hover {{ background: #C0392B; }}
                """)
                decline_btn.clicked.connect(lambda _, lrn=lrn, name=full_name: self._decline_student(lrn, name))

                action_layout.addWidget(approve_btn)
                action_layout.addWidget(decline_btn)
                self.apps_table.setCellWidget(r, 7, action_widget)
            else:
                self.apps_table.setItem(r, 7, QTableWidgetItem("—"))

        self.apps_table.resizeRowsToContents()

    def _load_approved(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT si.lrn_id, CONCAT(si.first_name,' ',COALESCE(si.middle_name,''),' ',si.last_name),
                       si.grade_level, si.strand, si.email, si.school_year
                FROM student_info si
                JOIN student_status ss ON si.lrn_id = ss.student_lrn
                WHERE ss.status = 'Approved'
            """)
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        self.approved_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.approved_table.setItem(r, c, QTableWidgetItem(str(val).strip()))

    def _load_announcements(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, title, target, posted_by, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i'), content
                FROM announcements ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        self.staff_ann_list.setRowCount(len(rows))
        self._ann_contents = {}
        for r, row in enumerate(rows):
            ann_id, title, target, posted_by, dt, content = row
            self._ann_contents[r] = content
            for c, val in enumerate([title, target, posted_by, dt]):
                self.staff_ann_list.setItem(r, c, QTableWidgetItem(str(val)))

    def _view_announcement(self, row, col):
        content = self._ann_contents.get(row, "")
        self.ann_content.setPlainText(content)

    def _refresh_dashboard(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            for status, card in [('Pending', self.card_pending), ('Approved', self.card_approved), ('Declined', self.card_declined)]:
                cur.execute("SELECT COUNT(*) FROM student_status WHERE status=%s", (status,))
                count = cur.fetchone()[0]
                card._value_label.setText(str(count))
        finally:
            cur.close()
            conn.close()

    # ── Actions ───────────────────────────────────────────────
    def _approve_student(self, lrn, name):
        dlg = FeedbackDialog(name, "Approve", self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            feedback = dlg.get_feedback()
            db = database()
            conn = db.connect()
            cur = conn.cursor()
            try:
                cur.execute(
                    "UPDATE student_status SET status='Approved', feedback=%s WHERE student_lrn=%s",
                    (feedback, lrn)
                )
                conn.commit()
                QMessageBox.information(self, "Approved", f"{name} has been approved.")
                self._load_students()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                cur.close()
                conn.close()

    def _decline_student(self, lrn, name):
        dlg = FeedbackDialog(name, "Decline", self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            feedback = dlg.get_feedback()
            db = database()
            conn = db.connect()
            cur = conn.cursor()
            try:
                cur.execute(
                    "UPDATE student_status SET status='Declined', feedback=%s WHERE student_lrn=%s",
                    (feedback, lrn)
                )
                conn.commit()
                QMessageBox.information(self, "Declined", f"{name}'s application has been declined.")
                self._load_students()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                cur.close()
                conn.close()

    def _logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            from views.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
