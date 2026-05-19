class Person:
    def __init__(self, name, age, id_number):
        self.name = name
        self.age = age
        self.id_number = id_number

    def display_info(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("ID Number:", self.id_number)


class Student(Person):
    def __init__(self, name, age, id_number, strand):
        super().__init__(name, age, id_number)
        self.strand = strand

    def display_info(self):
        super().display_info()
        print("Strand:", self.strand)
        print("-------------------")


class Teacher(Person):
    def __init__(self, name, age, id_number, subject):
        super().__init__(name, age, id_number)
        self.subject = subject

    def display_info(self):
        super().display_info()
        print("Subject:", self.subject)
        print("-------------------")


class SchoolClass:
    def __init__(self, class_name):
        self.class_name = class_name
        self.teacher = None
        self.students = []

    def add_student(self, student):
        if len(self.students) < 40:
            self.students.append(student)
            print("Student added to class.")
        else:
            print("Cannot add student. Class is full (40 max).")

    def assign_teacher(self, teacher):
        if self.teacher is None:
            self.teacher = teacher
            print("Teacher assigned to class.")
        else:
            print("This class already has a teacher.")

    def display_class(self):
        print("\nClass Name:", self.class_name)

        if self.teacher:
            print("\nTeacher Info:")
            self.teacher.display_info()
        else:
            print("No teacher assigned.")

        print("\nStudents:")
        if self.students:
            for student in self.students:
                student.display_info()
        else:
            print("No students in this class.")


class RegistrationSystem:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.classes = {}

    def add_student_to_class(self, student, class_name):
        if class_name in self.classes:
            self.classes[class_name].add_student(student)
        else:
            print("Class not found.")

    def assign_teacher_to_class(self, teacher, class_name):
        if class_name in self.classes:
            self.classes[class_name].assign_teacher(teacher)
        else:
            print("Class not found.")

    def view_all_students(self):
        print("\nALL STUDENTS:")
        for student in self.students:
            student.display_info()

    def view_all_teachers(self):
        print("\nALL TEACHERS:")
        for teacher in self.teachers:
            teacher.display_info()

    def view_all_classes(self):
        print("\nALL CLASSES:")
        for class_name in self.classes:
            print(class_name)

    def view_class(self, class_name):
        if class_name in self.classes:
            self.classes[class_name].display_class()
        else:
            print("Class not found.")


system = RegistrationSystem()

while True:
    print("\n===== SHS REGISTRATION SYSTEM MENU =====")
    print("1. Add Student")
    print("2. Add Teacher")
    print("3. Create Class")
    print("4. Assign Teacher to Class")
    print("5. Add Student to Class")
    print("6. View All Students")
    print("7. View All Teachers")
    print("8. View All Classes")
    print("9. View One Class")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Name: ")
        age = int(input("Age: "))
        id_number = input("ID Number: ")
        strand = input("Strand: ")
        student = Student(name, age, id_number, strand)
        system.students.append(student)
        print("Student added.")

    elif choice == "2":
        name = input("Name: ")
        age = int(input("Age: "))
        id_number = input("ID Number: ")
        subject = input("Subject: ")
        teacher = Teacher(name, age, id_number, subject)
        system.teachers.append(teacher)
        print("Teacher added.")

    elif choice == "3":
        class_name = input("Class Name (e.g. STEM-11A): ")
        system.classes[class_name] = SchoolClass(class_name)
        print("Class created.")

    elif choice == "4":
        class_name = input("Enter Class Name: ")
        if system.teachers:
            system.assign_teacher_to_class(system.teachers[0], class_name)
        else:
            print("No teachers available.")

    elif choice == "5":
        class_name = input("Enter Class Name: ")
        if system.students:
            system.add_student_to_class(system.students[0], class_name)
        else:
            print("No students available.")


    elif choice == "6":
        system.view_all_students()

    elif choice == "7":
        system.view_all_teachers()

    elif choice == "8":
        system.view_all_classes()

    elif choice == "9":
        class_name = input("Enter Class Name: ")
        system.view_class(class_name)

    elif choice == "0":
        print("Program ended.")
        break

    else:
        print("Invalid choice. Try again.")