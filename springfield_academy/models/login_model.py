import bcrypt
from springfield_academy.views.database_conn import database


class login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def _check(self, table, extra_join=None, extra_select=None):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            if table == 'student_credentials':
                sql = """
                    SELECT sc.password, ss.status
                    FROM student_credentials sc
                    JOIN student_status ss ON sc.student_lrn = ss.student_lrn
                    WHERE sc.username = %s
                """
                cur.execute(sql, (self.username,))
                row = cur.fetchone()
                if not row:
                    return 'not_found'
                stored, status = row
                ok = bcrypt.checkpw(self.password.encode(), stored.encode())
                if not ok:
                    return 'wrong_password'
                return status.lower()  # 'pending' | 'declined' | 'approved'
            else:
                sql = f"SELECT password FROM {table} WHERE username = %s"
                cur.execute(sql, (self.username,))
                row = cur.fetchone()
                if not row:
                    return 'not_found'
                ok = bcrypt.checkpw(self.password.encode(), row[0].encode())
                return 'approved' if ok else 'wrong_password'
        except Exception as e:
            print(f'Login error: {e}')
            return 'error'
        finally:
            cur.close()
            conn.close()

    def check_pass_student(self):
        return self._check('student_credentials')

    def check_pass_staff(self):
        return self._check('staff_credentials')

    def check_pass_admin(self):
        return self._check('admin_credentials')

    def get_student_lrn(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT student_lrn FROM student_credentials WHERE username=%s", (self.username,))
            row = cur.fetchone()
            return row[0] if row else None
        finally:
            cur.close()
            conn.close()

    def get_staff_info(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, full_name FROM staff_credentials WHERE username=%s", (self.username,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    def get_admin_info(self):
        db = database()
        conn = db.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, full_name FROM admin_credentials WHERE username=%s", (self.username,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()
