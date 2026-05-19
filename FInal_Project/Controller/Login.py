from FInal_Project.Model.database_conn import database
import bcrypt

class login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_pass_student(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()

        try:
            sql = """
                SELECT sc.password, ss.Status 
                FROM student_credentials sc
                JOIN student_status ss ON sc.student_lrn = ss.student_lrn
                WHERE sc.username = %s
            """
            cursor.execute(sql, (self.username,))
            result = cursor.fetchone()

            if result is None:
                return 'not_found'

            stored_password = result[0]
            status = result[1]

            is_correct = bcrypt.checkpw(
                self.password.encode('utf-8'),
                stored_password.encode('utf-8')
            )

            if not is_correct:
                return 'wrong_password'

            if status == 'Pending':
                return 'pending'
            elif status == 'Declined':
                return 'declined'
            elif status == 'Approved':
                return 'approved'

        except Exception as e:
            print(f'❌ Error: {e}')
            return 'error'

        finally:
            cursor.close()
            connection.close()

    # ─── Staff login ───────────────────────────────────────────────
    def check_pass_staff(self):
        """Returns True/False/'empty' for staff credentials stored in staff_credentials table."""
        db = database()
        connection = db.connect()
        cursor = connection.cursor()

        try:
            sql = """
                SELECT password FROM staff_credentials
                WHERE username = %s
            """
            cursor.execute(sql, (self.username,))
            result = cursor.fetchone()

            if result is None:
                return 'not_found'

            stored_password = result[0]
            is_correct = bcrypt.checkpw(
                self.password.encode('utf-8'),
                stored_password.encode('utf-8')
            )

            return 'approved' if is_correct else 'wrong_password'

        except Exception as e:
            print(f'❌ Error: {e}')
            return 'error'

        finally:
            cursor.close()
            connection.close()

    # ─── Admin login ───────────────────────────────────────────────
    def check_pass_admin(self):
        """Returns 'approved' / 'wrong_password' / 'not_found' / 'error' for admin accounts."""
        db = database()
        connection = db.connect()
        cursor = connection.cursor()

        try:
            sql = """
                SELECT password FROM admin_credentials
                WHERE username = %s
            """
            cursor.execute(sql, (self.username,))
            result = cursor.fetchone()

            if result is None:
                return 'not_found'

            stored_password = result[0]
            is_correct = bcrypt.checkpw(
                self.password.encode('utf-8'),
                stored_password.encode('utf-8')
            )

            return 'approved' if is_correct else 'wrong_password'

        except Exception as e:
            print(f'❌ Error: {e}')
            return 'error'

        finally:
            cursor.close()
            connection.close()