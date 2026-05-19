import tkinter as tk
from tkinter import ttk, messagebox

# Data storage
students = []
valid_strands = ["STEM", "ABM", "HUMSS", "TVL", "ARTS & DESIGN"]


# ---------------- FUNCTIONS ---------------- #
def enroll_student():
    name = entry_name.get().strip()
    grade = combo_grade.get()
    strand = combo_strand.get()

    # Validation
    if not name or not grade or not strand:
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return

    # Duplicate check
    for s in students:
        if s["name"].lower() == name.lower():
            messagebox.showerror("Duplicate", f"{name} is already enrolled.")
            return

    # Add student
    students.append({"name": name, "grade": grade, "strand": strand})
    messagebox.showinfo("Success", f"{name} enrolled in Grade {grade} ({strand}).")

    # Update list display
    update_student_list()
    clear_fields()


def update_student_list():
    listbox_students.delete(0, tk.END)
    for i, s in enumerate(students, start=1):
        listbox_students.insert(tk.END, f"{i}. {s['name']} - Grade {s['grade']} ({s['strand']})")


def clear_fields():
    entry_name.delete(0, tk.END)
    combo_grade.set('')
    combo_strand.set('')


def count_students():
    if not students:
        messagebox.showinfo("No Data", "No students enrolled yet.")
        return
    strand_count = {}
    for s in students:
        strand = s["strand"]
        strand_count[strand] = strand_count.get(strand, 0) + 1

    count_text = "\n".join([f"{strand}: {count}" for strand, count in strand_count.items()])
    messagebox.showinfo("Student Count", count_text)


def search_student():
    query = entry_search.get().strip().lower()
    if not query:
        messagebox.showwarning("Missing Info", "Please enter a name to search.")
        return

    for s in students:
        if s["name"].lower() == query:
            messagebox.showinfo("Found", f"{s['name']} - Grade {s['grade']} ({s['strand']})")
            return
    messagebox.showerror("Not Found", "Student not found.")


# ---------------- MAIN WINDOW ---------------- #
root = tk.Tk()
root.title("SHS Enrollment System")
root.geometry("600x500")
root.resizable(False, False)

# Title
lbl_title = tk.Label(root, text="Senior High School Enrollment System", font=("Arial", 16, "bold"))
lbl_title.pack(pady=10)

# Frame for enrollment form
frame_form = tk.Frame(root)
frame_form.pack(pady=5)

# Name
tk.Label(frame_form, text="Student Name:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_name = tk.Entry(frame_form, width=30)
entry_name.grid(row=0, column=1, pady=5)

# Grade Level
tk.Label(frame_form, text="Grade Level:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
combo_grade = ttk.Combobox(frame_form, values=["11", "12"], width=28, state="readonly")
combo_grade.grid(row=1, column=1, pady=5)

# Strand
tk.Label(frame_form, text="Strand:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
combo_strand = ttk.Combobox(frame_form, values=valid_strands, width=28, state="readonly")
combo_strand.grid(row=2, column=1, pady=5)

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_enroll = tk.Button(frame_buttons, text="Enroll Student", command=enroll_student, width=15, bg="#4CAF50", fg="white")
btn_enroll.grid(row=0, column=0, padx=5)

btn_count = tk.Button(frame_buttons, text="Count Students", command=count_students, width=15, bg="#2196F3", fg="white")
btn_count.grid(row=0, column=1, padx=5)

# Student list
tk.Label(root, text="Enrolled Students:", font=("Arial", 12, "bold")).pack(pady=5)
listbox_students = tk.Listbox(root, width=70, height=10)
listbox_students.pack()

# Search bar
frame_search = tk.Frame(root)
frame_search.pack(pady=10)

tk.Label(frame_search, text="Search Student:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
entry_search = tk.Entry(frame_search, width=30)
entry_search.grid(row=0, column=1, padx=5)
btn_search = tk.Button(frame_search, text="Search", command=search_student, width=10, bg="#FFC107")
btn_search.grid(row=0, column=2, padx=5)

# Footer
tk.Label(root, text="© 2025 SHS Enrollment System - Python Project", font=("Arial", 9), fg="gray").pack(side="bottom",
                                                                                                        pady=5)

# Run the window
root.mainloop()
