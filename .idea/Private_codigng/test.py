import json
from pathlib import Path
import datetime

DATA_FILE = Path("students.json")

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {"students": []}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def find_student(data, key):
    for s in data["students"]:
        if s.get("student_id") == key or s.get("lrn") == key:
            return s
    return None

def enroll_student(data):
    print("\n== SHS ENROLLMENT SYSTEM ==")
    key = input("Enter Student ID or LRN: ").strip()

    student = find_student(data, key)
    if not student:
        print("❌ Student not found in database.")
        return

    print(f"\nFound: {student['fullname']} | Current Status: {student.get('status')}")

    grade = input("Enroll to Grade (11 or 12): ").strip()
    if grade not in ("11", "12"):
        print("❌ Invalid grade level.")
        return

    section = input("Section Name: ").strip()
    subjects = input("Subjects (comma separated): ").split(",")
    subjects = [s.strip() for s in subjects if s.strip()]

    enrollment_record = {
        "date": datetime.datetime.now().isoformat(timespec='seconds'),
        "school_year": input("School Year (e.g. 2025-2026): ").strip(),
        "grade_level": grade,
        "section": section,
        "subjects": subjects
    }

    # Update student info
    student["grade_level"] = grade
    student["section"] = section
    student["status"] = "Enrolled"
    student.setdefault("enrollment_history", []).append(enrollment_record)

    save_data(data)

    print(f"\n✅ {student['fullname']} is now officially ENROLLED in Grade {grade}, Section {section}.")

def list_students(data):
    print("\n== All Students in Database ==")
    for s in data["students"]:
        print(f"- {s['fullname']} | ID: {s['student_id']} | Grade: {s.get('grade_level')} | Status: {s.get('status')}")

def menu():
    data = load_data()

    while True:
        print("\n----- SHS ENROLLMENT MENU -----")
        print("1) Enroll a student")
        print("2) List students")
        print("3) Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            enroll_student(data)
        elif choice == "2":
            list_students(data)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()
