from db_connection import database

class control:
    def __init__(self, student_id=None, name=None, course=None):
        self.student_id = student_id
        self.name = name
        self.course = course


    def Create_students(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()

        try:
            sql = """
            INSERT INTO students (student_id, name, course) VALUES (%s, %s, %s)
            """

            cursor.execute(sql, (self.student_id, self.name, self.course))
            connection.commit()
            print("✅ Credentials saved!")

        except Exception as e:
            connection.rollback()
            print(e)
        finally:
            cursor.close()
            connection.close()


    def Read_students(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()

        try:
            sql = """
                    SELECT * FROM students
                    """
            cursor.execute(sql)
            rows = cursor.fetchall()

            if not rows:
                print('No students found.')
                return

            print('{:<15} {:<20} {:<20}'.format('|Student_id|','|Name    |','|Course   |'))
            for row in rows:
                print('{:<15} {:<20} {:<20}'.format(row[0], row[1], row[2]))

            print("✅ Successful")

        except Exception as e:
            connection.rollback()
            print(e)
        finally:
            cursor.close()
            connection.close()


    def Update_students(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()

        try:
            fields = []
            values = []

            if self.name:  # skips if empty string
                fields.append("name = %s")
                values.append(self.name)

            if self.course:
                fields.append("course = %s")
                values.append(self.course)

            if not fields:
                print('Nothing to update — no fields were entered.')
                return

            values.append(self.student_id)

            sql = f"""
            UPDATE students SET {', '.join(fields)}  WHERE Student_id = %s
            """

            cursor.execute(sql, (values))

            connection.commit()

            if cursor.rowcount == 0:
                print(f'No student found with ID {self.student_id}.')
            else:
                print(f'✅ Student {self.student_id} updated successfully.')


        except Exception as e:
            connection.rollback()
            print(e)
        finally:
            cursor.close()
            connection.close()


    def Delete_students(self):
        db = database()
        connection = db.connect()
        cursor = connection.cursor()

        try:
            sql = """
                   DELETE FROM students WHERE Student_id = %s
                   """
            cursor.execute(sql, (self.student_id))

            connection.commit()

            if cursor.rowcount == 0:
                print(f'No student found with ID {self.student_id}.')
            else:
                print(f'✅ Student {self.student_id} deleted successfully.')


        except Exception as e:
            connection.rollback()
            print(e)
        finally:
            cursor.close()
            connection.close()