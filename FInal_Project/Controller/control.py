import bcrypt
from FInal_Project.Model.database_conn import database


class Students:
    def __init__(self, personal_info_lrn_input, personal_info_first_name_input,
                 personal_info_middle_name_input, personal_info_last_name_input,
                 personal_info_date_of_birth_input, personal_info_gender_input,
                 contact_info_email_input, contact_info_phone_input,
                 guardian_info_first_name_input, guardian_info_middle_name_input,
                 guardian_info_last_name_input, guardian_info_phone_number_input,
                 guardian_info_current_rel_input, academic_info_grade_level_input,
                 academic_info_strand_input, academic_info_semester_input,
                 academic_info_previous_school_input):

        self.personal_info_lrn_input            = personal_info_lrn_input
        self.personal_info_first_name_input      = personal_info_first_name_input
        self.personal_info_middle_name_input     = personal_info_middle_name_input
        self.personal_info_last_name_input       = personal_info_last_name_input
        self.personal_info_date_of_birth_input   = personal_info_date_of_birth_input
        self.personal_info_gender_input          = personal_info_gender_input
        self.contact_info_email_input            = contact_info_email_input
        self.contact_info_phone_input            = contact_info_phone_input
        self.guardian_info_first_name_input      = guardian_info_first_name_input
        self.guardian_info_middle_name_input     = guardian_info_middle_name_input
        self.guardian_info_last_name_input       = guardian_info_last_name_input
        self.guardian_info_phone_number_input    = guardian_info_phone_number_input
        self.guardian_info_current_rel_input     = guardian_info_current_rel_input
        self.academic_info_grade_level_input     = academic_info_grade_level_input
        self.academic_info_strand_input          = academic_info_strand_input
        self.academic_info_semester_input        = academic_info_semester_input
        self.academic_info_previous_school_input = academic_info_previous_school_input


    def Create_Student_Credentials(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            lrn      = self.personal_info_lrn_input
            username = self.contact_info_email_input        # email as username
            password = self.personal_info_lrn_input         # default pass = LRN

            hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            sql = """
                INSERT INTO Student_Credentials(Student_lrn, username, password)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (lrn, username, hashed_pass))
            connection.commit()
            print("✅ Credentials saved!")

        except Exception as e:
            connection.rollback()
            print(f"❌ Error saving credentials: {e}")
        finally:
            cursor.close()
            connection.close()

    def student_status(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO student_status(Student_lrn) VALUES (%s)"
            cursor.execute(sql, (self.personal_info_lrn_input,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f'ERROR: {e}')
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # ADD STUDENT — master insert
    # ─────────────────────────────────────────────────────────────────
    def add_student(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = """
                INSERT INTO StudentData(
                    student_lrn, First_name, Middle_name, Last_name,
                    Date_of_birth, Gender, Email_address, Phone_number,
                    Guardian_First_name, Guardian_Middle_name, Guardian_Last_name,
                    Guadian_Phone_Number, Current_Relationship,
                    Grade_level, Strand, Semester, Previous_school
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            cursor.execute(sql, (
                self.personal_info_lrn_input,
                self.personal_info_first_name_input,
                self.personal_info_middle_name_input,
                self.personal_info_last_name_input,
                self.personal_info_date_of_birth_input,
                self.personal_info_gender_input,
                self.contact_info_email_input,
                self.contact_info_phone_input,
                self.guardian_info_first_name_input,
                self.guardian_info_middle_name_input,
                self.guardian_info_last_name_input,
                self.guardian_info_phone_number_input,
                self.guardian_info_current_rel_input,
                self.academic_info_grade_level_input,
                self.academic_info_strand_input,
                self.academic_info_semester_input,
                self.academic_info_previous_school_input,
            ))
            connection.commit()
            print("✅ Student saved!")

            self.Create_Student_Credentials()
            self.student_status()

        except Exception as e:
            connection.rollback()
            print(f"❌ Error adding student: {e}")
            raise
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # GET student data by LRN
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def get_student_by_lrn(lrn: str) -> dict | None:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM StudentData WHERE student_lrn = %s"
            cursor.execute(sql, (lrn,))
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        except Exception as e:
            print(f'❌ Error fetching student: {e}')
            return None
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # GET LRN by username/email
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def get_lrn_by_username(username: str) -> str | None:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = "SELECT student_lrn FROM Student_Credentials WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f'❌ Error fetching LRN: {e}')
            return None
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # GET ALL STUDENTS
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def get_all_students() -> list[dict]:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = """
                SELECT
                    sd.student_lrn,
                    sd.First_name,
                    sd.Middle_name,
                    sd.Last_name,
                    sd.Date_of_birth,
                    sd.Gender,
                    sd.Email_address,
                    sd.Phone_number,
                    sd.Guardian_First_name,
                    sd.Guardian_Middle_name,
                    sd.Guardian_Last_name,
                    sd.Guadian_Phone_Number,
                    sd.Current_Relationship,
                    sd.Grade_level,
                    sd.Strand,
                    sd.Semester,
                    sd.Previous_school,
                    ss.Status
                FROM StudentData sd
                LEFT JOIN Student_Status ss ON sd.student_lrn = ss.Student_lrn
                ORDER BY sd.Last_name, sd.First_name
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f'❌ Error fetching all students: {e}')
            return []
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # GET STUDENTS FILTERED BY STATUS
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def get_students_by_status(status: str) -> list[dict]:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = """
                SELECT
                    sd.student_lrn,
                    sd.First_name,
                    sd.Last_name,
                    sd.Grade_level,
                    sd.Strand,
                    sd.Semester,
                    sd.Email_address,
                    ss.Status
                FROM StudentData sd
                LEFT JOIN Student_Status ss ON sd.student_lrn = ss.Student_lrn
                WHERE ss.Status = %s
                ORDER BY sd.Last_name, sd.First_name
            """
            cursor.execute(sql, (status,))
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f'❌ Error: {e}')
            return []
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # UPDATE STATUS
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def update_student_status(lrn: str, new_status: str) -> bool:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = "UPDATE Student_Status SET Status = %s WHERE Student_lrn = %s"
            cursor.execute(sql, (new_status, lrn))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f'❌ Error updating status: {e}')
            return False
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # DELETE STUDENT
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def delete_student(lrn: str) -> bool:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = "DELETE FROM StudentData WHERE student_lrn = %s"
            cursor.execute(sql, (lrn,))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f'❌ Error deleting student: {e}')
            return False
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # UPDATE STUDENT INFO
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def update_student(lrn: str, fields: dict) -> bool:
        if not fields:
            return False
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            set_clause = ", ".join(f"{col} = %s" for col in fields.keys())
            values = list(fields.values()) + [lrn]
            sql = f"UPDATE StudentData SET {set_clause} WHERE student_lrn = %s"
            cursor.execute(sql, values)
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f'❌ Error updating student: {e}')
            return False
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # SEARCH STUDENTS
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def search_students(keyword: str) -> list[dict]:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            like = f"%{keyword}%"
            sql = """
                SELECT
                    sd.student_lrn,
                    sd.First_name,
                    sd.Last_name,
                    sd.Grade_level,
                    sd.Strand,
                    sd.Semester,
                    sd.Email_address,
                    ss.Status
                FROM StudentData sd
                LEFT JOIN Student_Status ss ON sd.student_lrn = ss.Student_lrn
                WHERE
                    sd.student_lrn   LIKE %s OR
                    sd.First_name    LIKE %s OR
                    sd.Last_name     LIKE %s OR
                    sd.Strand        LIKE %s OR
                    sd.Email_address LIKE %s
                ORDER BY sd.Last_name, sd.First_name
            """
            cursor.execute(sql, (like, like, like, like, like))
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f'❌ Error searching students: {e}')
            return []
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # COUNT HELPERS  (Dashboard stats)
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def count_by_status() -> dict:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = """
                SELECT Status, COUNT(*) as cnt
                FROM Student_Status
                GROUP BY Status
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            counts = {'Pending': 0, 'Approved': 0, 'Declined': 0}
            for status, cnt in rows:
                if status in counts:
                    counts[status] = cnt
            counts['Total'] = sum(counts.values())
            return counts
        except Exception as e:
            print(f'❌ Error counting: {e}')
            return {'Pending': 0, 'Approved': 0, 'Declined': 0, 'Total': 0}
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # COUNT ENROLLED THIS WEEK  (for pie chart)
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def count_enrolled_this_week() -> dict:
        """
        Returns {'this_week': n, 'before': n} based on when students were
        added.  Looks for a created_at / enrolled_date column; falls back
        to counting all Approved if no date column exists.
        """
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            # Try with a date column — adjust column name to match your schema
            sql = """
                SELECT
                    SUM(CASE WHEN sd.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                             THEN 1 ELSE 0 END) AS this_week,
                    SUM(CASE WHEN sd.created_at <  DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                             THEN 1 ELSE 0 END) AS before
                FROM StudentData sd
                JOIN Student_Status ss ON sd.student_lrn = ss.Student_lrn
                WHERE ss.Status = 'Approved'
            """
            cursor.execute(sql)
            row = cursor.fetchone()
            return {
                'this_week': int(row[0] or 0),
                'before':    int(row[1] or 0),
            }
        except Exception:
            # Fallback: no date column — just count approved vs rest
            try:
                cursor.execute("""
                    SELECT
                        SUM(CASE WHEN Status = 'Approved' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN Status != 'Approved' THEN 1 ELSE 0 END)
                    FROM Student_Status
                """)
                row = cursor.fetchone()
                return {
                    'this_week': int(row[0] or 0),
                    'before':    int(row[1] or 0),
                }
            except Exception as e2:
                print(f'❌ Error counting weekly: {e2}')
                return {'this_week': 0, 'before': 0}
        finally:
            cursor.close()
            connection.close()

    # ─────────────────────────────────────────────────────────────────
    # SUBJECTS — fetch by strand + grade level
    # Each strand has its own table: gas_subjects, stem_subjects, etc.
    # ─────────────────────────────────────────────────────────────────
    @staticmethod
    def get_subjects(strand: str, grade_level: str, semester: str = '') -> list[dict]:
        """
        Returns subjects for the student's strand and grade level.
        Maps strand name to the correct DB table:
          STEM   → stem_subjects
          ABM    → abm_subjects
          GAS    → gas_subjects
          HUMSS  → humss_subjects
          TVL    → tvl_subjects
        Each table has columns: subject_id, subject_name, grade_level, semester, units
        """
        STRAND_TABLE_MAP = {
            'STEM':  'stem_subjects',
            'ABM':   'abm_subjects',
            'GAS':   'gas_subjects',
            'HUMSS': 'humss_subjects',
            'TVL':   'tvl_subjects',
        }

        table = STRAND_TABLE_MAP.get(strand.upper() if strand else '')
        if not table:
            print(f'⚠️  Unknown strand: {strand}')
            return []

        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            if semester:
                sql = f"""
                    SELECT subject_id, subject_name, grade_level, semester, units
                    FROM {table}
                    WHERE grade_level = %s AND semester = %s
                    ORDER BY subject_id
                """
                cursor.execute(sql, (grade_level, semester))
            else:
                sql = f"""
                    SELECT subject_id, subject_name, grade_level, semester, units
                    FROM {table}
                    WHERE grade_level = %s
                    ORDER BY
                        CASE semester
                            WHEN '1st Semester' THEN 1
                            WHEN '2nd Semester' THEN 2
                            ELSE 3
                        END,
                        subject_id
                """
                cursor.execute(sql, (grade_level,))
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f'❌ Error fetching subjects from {table}: {e}')
            return []
        finally:
            cursor.close()
            connection.close()


# ══════════════════════════════════════════════════════════════════
#  ANNOUNCEMENTS
# ══════════════════════════════════════════════════════════════════
class Announcement:
    def __init__(self, title: str, content: str, target: str, posted_by: str):
        self.title     = title
        self.content   = content
        self.target    = target    # 'All' | 'Student' | 'Staff'
        self.posted_by = posted_by

    def post(self) -> bool:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = """
                INSERT INTO announcements (title, content, target, posted_by)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (self.title, self.content, self.target, self.posted_by))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f'❌ Error posting announcement: {e}')
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all() -> list[dict]:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = """
                SELECT id, title, content, target, posted_by, posted_date
                FROM announcements
                ORDER BY posted_date DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f'❌ Error fetching announcements: {e}')
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_for_target(target: str) -> list[dict]:
        """target: 'Student' | 'Staff' — also returns rows where target='All'"""
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            sql = """
                SELECT id, title, content, target, posted_by, posted_date
                FROM announcements
                WHERE target = 'All' OR target = %s
                ORDER BY posted_date DESC
            """
            cursor.execute(sql, (target,))
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f'❌ Error fetching announcements: {e}')
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(announcement_id: int) -> bool:
        db = database()
        connection = db.connect()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM announcements WHERE id = %s", (announcement_id,))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f'❌ Error deleting announcement: {e}')
            return False
        finally:
            cursor.close()
            connection.close()