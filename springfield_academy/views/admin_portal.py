import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QStackedWidget, QHeaderView, QGroupBox, QScrollArea,
    QTabWidget, QMessageBox, QComboBox, QLineEdit, QFormLayout,
    QDialog, QDialogButtonBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import bcrypt

from styles.theme import APP_STYLE, COLORS, SIDEBAR_STYLE
from database_conn import database


class CreateAccountDialog(QDialog):
    def __init__(self, role, parent=None):
        super().__init__(parent)
        self.role = role
        self.setWindowTitle(f"Create {role} Account")
        self.setMinimumWidth(420)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(f"New {role} Account")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {COLORS['primary']};")

        form = QFormLayout()
        self.full_name = QLineEdit(); self.full_name.setPlaceholderText("Full Name")
        self.email     = QLineEdit(); self.email.setPlaceholderText("Email Address")
        self.username  = QLineEdit(); self.username.setPlaceholderText("Username")
        self.password  = QLineEdit(); self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Password (min 6 chars)")
        self.confirm   = QLineEdit(); self.confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm.setPlaceholderText("Confirm Password")

        form.addRow("Full Name *", self.full_name)
        form.addRow("Email *", self.email)
        form.addRow("Username *", self.username)
        form.addRow("Password *", self.password)
        form.addRow("Confirm *", self.confirm)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._validate)
        btns.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(btns)

    def _validate(self):
        if not all([self.full_name.text().strip(), self.email.text().strip(),
                    self.username.text().strip(), self.password.text()]):
            QMessageBox.warning(self, "Missing Fields", "Please fill all required fields.")
            return
        if self.password.text() != self.confirm.text():
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return
        if len(self.password.text()) < 6:
            QMessageBox.warning(self, "Weak Password", "Password must be at least 6 characters.")
            return
        self.accept()

    def get_data(self):
        return {
            'full_name': self.full_name.text().strip(),
            'email': self.email.text().strip(),
            'username': self.username.text().strip(),
            'password': self.password.text(),
        }


class AdminPortal(QMainWindow):
    def __init__(self, admin_info, username):
        super().__init__()
        self.admin_info = admin_info
        self.username = username
        self.admin_name = admin_info[1] if admin_info else username

        self.setWindowTitle(f"Springfield Academy — Admin Portal ({self.admin_name})")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet(APP_STYLE + SIDEBAR_STYLE)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QHBoxLayout(central)
        main.setSpacing(0)
        main.setContentsMargins(0, 0, 0, 0)

        # ── Sidebar ──────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(12, 20, 12, 20)
        sb.setSpacing(4)

        school_lbl = QLabel("Springfield\nAcademy")
        school_lbl.setStyleSheet("color: white; font-size: 16px; font-weight: 800; padding: 8px 4px;")
        admin_lbl = QLabel(f"⚙️ {self.admin_name}")
        admin_lbl.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 11px; padding: 0 4px 12px 4px;")

        self.nav_buttons = {}
        nav_items = [
            ("dashboard",     "🏠  Dashboard"),
            ("announcements", "📢  Announcements"),
            ("students",      "👥  Students"),
            ("accounts",      "🔑  Manage Accounts"),
            ("reports",       "📄  Reports"),
        ]

        sb.addWidget(school_lbl)
        sb.addWidget(admin_lbl)

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
        pages = [
            self._build_dashboard(),
            self._build_announcements(),
            self._build_students(),
            self._build_accounts(),
            self._build_reports(),
        ]
        for p in pages:
            self.content_stack.addWidget(p)

        self.page_index = {
            "dashboard": 0, "announcements": 1, "students": 2, "accounts": 3, "reports": 4
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

        title = QLabel(f"Welcome, {self.admin_name} ⚙️")
        title.setObjectName("section_title")

        cards_row = QHBoxLayout()
        self.c_enrolled  = self._stat_card("Total Enrolled", "0", COLORS['primary'])
        self.c_pending   = self._stat_card("Pending", "0", COLORS['warning'])
        self.c_approved  = self._stat_card("Approved", "0", COLORS['success'])
        self.c_declined  = self._stat_card("Declined", "0", COLORS['danger'])
        self.c_staff     = self._stat_card("Staff Accounts", "0", COLORS['secondary'])
        for card in [self.c_enrolled, self.c_pending, self.c_approved, self.c_declined, self.c_staff]:
            cards_row.addWidget(card)

        layout.addWidget(title)
        layout.addLayout(cards_row)
        layout.addStretch()
        return page

    def _stat_card(self, label, value, color):
        card = QGroupBox()
        card.setStyleSheet(f"""
            QGroupBox {{
                background: white; border: none;
                border-left: 5px solid {color};
                border-radius: 8px; padding: 16px;
            }}
        """)
        cl = QVBoxLayout(card)
        val_lbl = QLabel(value)
        val_lbl.setStyleSheet(f"font-size: 30px; font-weight: 800; color: {color};")
        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-size: 12px; color: {COLORS['text_muted']}; font-weight: 600;")
        lbl.setWordWrap(True)
        cl.addWidget(val_lbl)
        cl.addWidget(lbl)
        card._value_label = val_lbl
        return card

    # ── Announcements ─────────────────────────────────────────
    def _build_announcements(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("Announcements")
        title.setObjectName("section_title")

        # Compose form
        compose = QGroupBox("Post New Announcement")
        cl = QVBoxLayout(compose)
        cl.setSpacing(10)

        row1 = QHBoxLayout()
        self.ann_title = QLineEdit(); self.ann_title.setPlaceholderText("Announcement Title")
        self.ann_target = QComboBox()
        self.ann_target.addItems(["both", "student", "staff"])
        row1.addWidget(QLabel("Title:")); row1.addWidget(self.ann_title, 2)
        row1.addWidget(QLabel("  Target:")); row1.addWidget(self.ann_target)

        self.ann_body = QTextEdit()
        self.ann_body.setPlaceholderText("Write your announcement here...")
        self.ann_body.setMaximumHeight(120)

        post_btn = QPushButton("📢 Post Announcement")
        post_btn.clicked.connect(self._post_announcement)

        cl.addLayout(row1)
        cl.addWidget(self.ann_body)
        cl.addWidget(post_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # List
        self.ann_list = QTableWidget()
        self.ann_list.setColumnCount(5)
        self.ann_list.setHorizontalHeaderLabels(["Title", "Target", "Posted By", "Date", "Action"])
        self.ann_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ann_list.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.ann_list.verticalHeader().setVisible(False)
        self.ann_list.setAlternatingRowColors(True)

        layout.addWidget(title)
        layout.addWidget(compose)
        layout.addWidget(QLabel("All Announcements:"))
        layout.addWidget(self.ann_list)
        return page

    # ── Students ──────────────────────────────────────────────
    def _build_students(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("All Students")
        title.setObjectName("section_title")
        refresh = QPushButton("🔄 Refresh")
        refresh.clicked.connect(self._load_students)
        hdr.addWidget(title); hdr.addStretch(); hdr.addWidget(refresh)

        self.students_table = QTableWidget()
        self.students_table.setColumnCount(8)
        self.students_table.setHorizontalHeaderLabels([
            "LRN", "Full Name", "Grade", "Strand", "Email", "Phone", "School Year", "Status"
        ])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.students_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.students_table.verticalHeader().setVisible(False)
        self.students_table.setAlternatingRowColors(True)

        layout.addLayout(hdr)
        layout.addWidget(self.students_table)
        return page

    # ── Accounts ──────────────────────────────────────────────
    def _build_accounts(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Manage Accounts")
        title.setObjectName("section_title")

        btn_row = QHBoxLayout()
        staff_btn = QPushButton("➕ Create Staff Account")
        admin_btn = QPushButton("➕ Create Admin Account")
        admin_btn.setObjectName("outline_btn")
        staff_btn.clicked.connect(lambda: self._create_account("Staff"))
        admin_btn.clicked.connect(lambda: self._create_account("Admin"))
        btn_row.addWidget(staff_btn); btn_row.addWidget(admin_btn); btn_row.addStretch()

        tabs = QTabWidget()
        self.staff_table = self._accounts_table()
        self.admin_table = self._accounts_table()
        tabs.addTab(self.staff_table, "Staff Accounts")
        tabs.addTab(self.admin_table, "Admin Accounts")

        layout.addWidget(title)
        layout.addLayout(btn_row)
        layout.addWidget(tabs)
        return page

    def _accounts_table(self):
        tbl = QTableWidget()
        tbl.setColumnCount(4)
        tbl.setHorizontalHeaderLabels(["Username", "Full Name", "Email", "Created At"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.verticalHeader().setVisible(False)
        tbl.setAlternatingRowColors(True)
        return tbl

    # ── Reports ───────────────────────────────────────────────
    def _build_reports(self):
        page = QWidget()
        page.setStyleSheet(f"background: {COLORS['light_bg']};")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Generate Reports")
        title.setObjectName("section_title")
        subtitle = QLabel("Export enrollment data as a PDF with charts and tables.")
        subtitle.setStyleSheet(f"color: {COLORS['text_muted']};")

        options_box = QGroupBox("Report Options")
        options_layout = QVBoxLayout(options_box)

        self.report_type = QComboBox()
        self.report_type.addItems([
            "Full Enrollment Report (All Students + Charts)",
            "Pending Applications Report",
            "Approved Students Report",
            "Students by Strand Report",
        ])
        options_layout.addWidget(QLabel("Select Report Type:"))
        options_layout.addWidget(self.report_type)

        gen_btn = QPushButton("📄 Generate & Export PDF")
        gen_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 700;
                min-height: 44px;
            }}
            QPushButton:hover {{ background: {COLORS['secondary']}; }}
        """)
        gen_btn.clicked.connect(self._generate_report)

        self.report_status = QLabel("")
        self.report_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: 600;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(options_box)
        layout.addWidget(gen_btn)
        layout.addWidget(self.report_status)
        layout.addStretch()
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
        elif key == "announcements":
            self._load_announcements()
        elif key == "students":
            self._load_students()
        elif key == "accounts":
            self._load_accounts()

    # ── Data / Actions ────────────────────────────────────────
    def _refresh_dashboard(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM student_info")
            self.c_enrolled._value_label.setText(str(cur.fetchone()[0]))
            for status, card in [('Pending', self.c_pending), ('Approved', self.c_approved), ('Declined', self.c_declined)]:
                cur.execute("SELECT COUNT(*) FROM student_status WHERE status=%s", (status,))
                card._value_label.setText(str(cur.fetchone()[0]))
            cur.execute("SELECT COUNT(*) FROM staff_credentials")
            self.c_staff._value_label.setText(str(cur.fetchone()[0]))
        finally:
            cur.close()
            conn.close()

    def _load_announcements(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, title, target, posted_by, DATE_FORMAT(created_at,'%Y-%m-%d %H:%i')
                FROM announcements ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        self.ann_list.setRowCount(len(rows))
        self._ann_ids = {}
        for r, row in enumerate(rows):
            ann_id, title, target, posted_by, dt = row
            self._ann_ids[r] = ann_id
            for c, val in enumerate([title, target, posted_by, dt]):
                self.ann_list.setItem(r, c, QTableWidgetItem(str(val)))
            del_btn = QPushButton("🗑 Delete")
            del_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {COLORS['danger']}; color: white;
                    border-radius: 4px; padding: 3px 10px;
                    font-size: 11px; font-weight: 600; min-height: 24px;
                }}
                QPushButton:hover {{ background: #C0392B; }}
            """)
            del_btn.clicked.connect(lambda _, aid=ann_id: self._delete_announcement(aid))
            self.ann_list.setCellWidget(r, 4, del_btn)

    def _post_announcement(self):
        title = self.ann_title.text().strip()
        body  = self.ann_body.toPlainText().strip()
        target = self.ann_target.currentText()

        if not title or not body:
            QMessageBox.warning(self, "Missing Fields", "Please fill in the title and content.")
            return

        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO announcements (title, content, target, posted_by) VALUES (%s,%s,%s,%s)",
                (title, body, target, self.admin_name)
            )
            conn.commit()
            self.ann_title.clear()
            self.ann_body.clear()
            QMessageBox.information(self, "Posted ✅", "Announcement posted successfully.")
            self._load_announcements()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            cur.close()
            conn.close()

    def _delete_announcement(self, ann_id):
        reply = QMessageBox.question(self, "Delete", "Delete this announcement?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            db = database()
            conn = db.connect()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM announcements WHERE id=%s", (ann_id,))
                conn.commit()
                self._load_announcements()
            finally:
                cur.close()
                conn.close()

    def _load_students(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT si.lrn_id, CONCAT(si.first_name,' ',COALESCE(si.middle_name,''),' ',si.last_name),
                       si.grade_level, si.strand, si.email, si.phone, si.school_year, ss.status
                FROM student_info si
                JOIN student_status ss ON si.lrn_id = ss.student_lrn
                ORDER BY si.registered_at DESC
            """)
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        self.students_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val or '').strip())
                if c == 7:  # Status column
                    if val == 'Approved': item.setForeground(QColor(COLORS['success']))
                    elif val == 'Pending': item.setForeground(QColor(COLORS['warning']))
                    elif val == 'Declined': item.setForeground(QColor(COLORS['danger']))
                self.students_table.setItem(r, c, item)

    def _load_accounts(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            for table, tbl_widget in [('staff_credentials', self.staff_table), ('admin_credentials', self.admin_table)]:
                cur.execute(f"SELECT username, full_name, email, DATE_FORMAT(created_at,'%Y-%m-%d') FROM {table} ORDER BY created_at DESC")
                rows = cur.fetchall()
                tbl_widget.setRowCount(len(rows))
                for r, row in enumerate(rows):
                    for c, val in enumerate(row):
                        tbl_widget.setItem(r, c, QTableWidgetItem(str(val or '')))
        finally:
            cur.close()
            conn.close()

    def _create_account(self, role):
        dlg = CreateAccountDialog(role, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
            table = 'staff_credentials' if role == 'Staff' else 'admin_credentials'

            db = database()
            conn = db.connect()
            cur = conn.cursor()
            try:
                cur.execute(
                    f"INSERT INTO {table} (username, full_name, email, password) VALUES (%s,%s,%s,%s)",
                    (data['username'], data['full_name'], data['email'], hashed)
                )
                conn.commit()
                QMessageBox.information(self, "Created ✅", f"{role} account '{data['username']}' created.")
                self._load_accounts()
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    QMessageBox.warning(self, "Duplicate", "Username already exists.")
                else:
                    QMessageBox.critical(self, "Error", str(e))
            finally:
                cur.close()
                conn.close()

    # ── PDF Report ────────────────────────────────────────────
    def _generate_report(self):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet

        report_type = self.report_type.currentText()

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", os.path.expanduser("~/Desktop/enrollment_report.pdf"),
            "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        # Fetch data
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM student_info"); total = cur.fetchone()[0]
            status_counts = {}
            for s in ['Pending', 'Approved', 'Declined']:
                cur.execute("SELECT COUNT(*) FROM student_status WHERE status=%s", (s,))
                status_counts[s] = cur.fetchone()[0]

            cur.execute("""
                SELECT si.strand, COUNT(*) FROM student_info si
                JOIN student_status ss ON si.lrn_id = ss.student_lrn
                WHERE ss.status = 'Approved'
                GROUP BY si.strand
            """)
            strand_data = dict(cur.fetchall())

            if "Pending" in report_type:
                cur.execute("""
                    SELECT si.lrn_id, CONCAT(si.first_name,' ',si.last_name), si.grade_level, si.strand, si.email, ss.status
                    FROM student_info si JOIN student_status ss ON si.lrn_id = ss.student_lrn
                    WHERE ss.status = 'Pending'
                """)
            elif "Approved" in report_type:
                cur.execute("""
                    SELECT si.lrn_id, CONCAT(si.first_name,' ',si.last_name), si.grade_level, si.strand, si.email, ss.status
                    FROM student_info si JOIN student_status ss ON si.lrn_id = ss.student_lrn
                    WHERE ss.status = 'Approved'
                """)
            else:
                cur.execute("""
                    SELECT si.lrn_id, CONCAT(si.first_name,' ',si.last_name), si.grade_level, si.strand, si.email, ss.status
                    FROM student_info si JOIN student_status ss ON si.lrn_id = ss.student_lrn
                    ORDER BY si.registered_at DESC
                """)
            student_rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        # Generate charts
        chart_paths = []

        # Pie chart — enrollment status
        tmp1 = os.path.join(tempfile.gettempdir(), 'chart_status.png')
        fig, ax = plt.subplots(figsize=(5, 4))
        labels = list(status_counts.keys())
        sizes  = list(status_counts.values())
        chart_colors = ['#F39C12', '#27AE60', '#E74C3C']
        if sum(sizes) > 0:
            ax.pie(sizes, labels=labels, colors=chart_colors, autopct='%1.1f%%',
                   startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        ax.set_title('Enrollment Status Distribution', fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(tmp1, dpi=150, bbox_inches='tight')
        plt.close()
        chart_paths.append(tmp1)

        # Bar chart — students by strand
        if strand_data:
            tmp2 = os.path.join(tempfile.gettempdir(), 'chart_strand.png')
            fig, ax = plt.subplots(figsize=(6, 4))
            strands = list(strand_data.keys())
            counts  = list(strand_data.values())
            bars = ax.bar(strands, counts, color='#1B3A6B', edgecolor='white', linewidth=1.5)
            ax.bar_label(bars, padding=3, fontsize=10, fontweight='bold')
            ax.set_title('Approved Students by Strand', fontsize=13, fontweight='bold')
            ax.set_xlabel('Strand'); ax.set_ylabel('Number of Students')
            ax.set_facecolor('#F8F9FA')
            plt.tight_layout()
            plt.savefig(tmp2, dpi=150, bbox_inches='tight')
            plt.close()
            chart_paths.append(tmp2)

        # Build PDF
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))
        elements = []

        elements.append(Paragraph("🏫 Springfield Academy", styles['Title']))
        elements.append(Paragraph(report_type, styles['Heading2']))
        elements.append(Paragraph(f"Generated by: {self.admin_name}", styles['Normal']))
        elements.append(Spacer(1, 10))

        # Summary stats
        summary_data = [['Metric', 'Count'],
                        ['Total Enrolled', str(total)],
                        ['Pending', str(status_counts.get('Pending', 0))],
                        ['Approved', str(status_counts.get('Approved', 0))],
                        ['Declined', str(status_counts.get('Declined', 0))]]
        stbl = Table(summary_data, colWidths=[180, 80])
        stbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B3A6B')),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 10),
            ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
            ('GRID',       (0,0), (-1,-1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('PADDING',    (0,0), (-1,-1), 8),
        ]))
        elements.append(Paragraph("Summary", styles['Heading3']))
        elements.append(stbl)
        elements.append(Spacer(1, 16))

        # Charts side by side
        if os.path.exists(chart_paths[0]):
            elements.append(Paragraph("Charts", styles['Heading3']))
            img_row = [[Image(chart_paths[0], width=240, height=190)]]
            if len(chart_paths) > 1 and os.path.exists(chart_paths[1]):
                img_row[0].append(Image(chart_paths[1], width=290, height=190))
            chart_table = Table(img_row)
            elements.append(chart_table)
            elements.append(Spacer(1, 16))

        # Student table
        elements.append(Paragraph("Student List", styles['Heading3']))
        tbl_data = [['LRN', 'Full Name', 'Grade', 'Strand', 'Email', 'Status']]
        for row in student_rows:
            tbl_data.append([str(v or '') for v in row])

        col_widths = [80, 150, 55, 60, 160, 60]
        main_table = Table(tbl_data, colWidths=col_widths)
        main_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B3A6B')),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 9),
            ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
            ('GRID',       (0,0), (-1,-1), 0.4, colors.grey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('PADDING',    (0,0), (-1,-1), 6),
        ]))
        elements.append(main_table)

        doc.build(elements)

        # Cleanup
        for p in chart_paths:
            if os.path.exists(p):
                os.remove(p)

        self.report_status.setText(f"✅ Report saved to: {file_path}")
        QMessageBox.information(self, "Report Generated! ✅",
            f"Your PDF report has been saved to:\n{file_path}")

    def _logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            from views.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
