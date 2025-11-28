import tkinter as tk
from tkinter import messagebox, simpledialog
import statistics

# -------------------------------------------------------
# Load student data from file
# -------------------------------------------------------
def load_students():
    students = []
    try:
        with open("Assessment 1 - Skills Portfolio/A1 - Resources/studentMarks.txt", "r") as file:
            n = int(file.readline().strip())  # number of students
            for line in file:
                parts = line.strip().split(",")
                code = parts[0]
                name = parts[1]
                c1, c2, c3, exam = map(int, parts[2:])
                coursework_total = c1 + c2 + c3  # out of 60
                total = coursework_total + exam  # out of 160
                percent = (total / 160) * 100

                # Determine grade
                if percent >= 70:
                    grade = "A"
                elif percent >= 60:
                    grade = "B"
                elif percent >= 50:
                    grade = "C"
                elif percent >= 40:
                    grade = "D"
                else:
                    grade = "F"

                students.append({
                    "code": code,
                    "name": name,
                    "coursework": coursework_total,
                    "exam": exam,
                    "total": total,
                    "percent": percent,
                    "grade": grade
                })
        return students
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found!")
        return []

# -------------------------------------------------------
# Display area update
# -------------------------------------------------------
def display(text):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")

# -------------------------------------------------------
# Menu Functions
# -------------------------------------------------------
def view_all():
    if not students:
        return
    text = ""
    percentages = []
    for s in students:
        text += f"Name: {s['name']}\n"
        text += f"Student Number: {s['code']}\n"
        text += f"Coursework Total: {s['coursework']} / 60\n"
        text += f"Exam Mark: {s['exam']} / 100\n"
        text += f"Overall Percentage: {s['percent']:.2f}%\n"
        text += f"Grade: {s['grade']}\n"
        text += "-"*40 + "\n"
        percentages.append(s['percent'])

    avg = statistics.mean(percentages)
    text += f"\nTotal Students: {len(students)}"
    text += f"\nAverage Percentage: {avg:.2f}%"

    display(text)

def view_individual():
    if not students:
        return
    code = simpledialog.askstring("Student Search", "Enter student number:")
    if not code:
        return
    for s in students:
        if s["code"] == code:
            text = (
                f"Name: {s['name']}\n"
                f"Student Number: {s['code']}\n"
                f"Coursework Total: {s['coursework']} / 60\n"
                f"Exam Mark: {s['exam']} / 100\n"
                f"Overall Percentage: {s['percent']:.2f}%\n"
                f"Grade: {s['grade']}"
            )
            display(text)
            return

    messagebox.showinfo("Not Found", "No student found with that number.")

def show_highest():
    if not students:
        return
    s = max(students, key=lambda x: x["total"])
    text = (
        f"Highest Mark Student:\n"
        f"Name: {s['name']}\n"
        f"Student Number: {s['code']}\n"
        f"Coursework Total: {s['coursework']} / 60\n"
        f"Exam Mark: {s['exam']} / 100\n"
        f"Overall Percentage: {s['percent']:.2f}%\n"
        f"Grade: {s['grade']}"
    )
    display(text)

def show_lowest():
    if not students:
        return
    s = min(students, key=lambda x: x["total"])
    text = (
        f"Lowest Mark Student:\n"
        f"Name: {s['name']}\n"
        f"Student Number: {s['code']}\n"
        f"Coursework Total: {s['coursework']} / 60\n"
        f"Exam Mark: {s['exam']} / 100\n"
        f"Overall Percentage: {s['percent']:.2f}%\n"
        f"Grade: {s['grade']}"
    )
    display(text)

# -------------------------------------------------------
# Tkinter GUI
# -------------------------------------------------------
window = tk.Tk()
window.title("Student Manager")
window.geometry("600x500")

students = load_students()

frame = tk.Frame(window)
frame.pack(pady=10)

btn1 = tk.Button(frame, text="1. View All Students", width=25, command=view_all)
btn2 = tk.Button(frame, text="2. View Individual Student", width=25, command=view_individual)
btn3 = tk.Button(frame, text="3. Highest Score", width=25, command=show_highest)
btn4 = tk.Button(frame, text="4. Lowest Score", width=25, command=show_lowest)

btn1.grid(row=0, column=0, padx=5, pady=5)
btn2.grid(row=1, column=0, padx=5, pady=5)
btn3.grid(row=2, column=0, padx=5, pady=5)
btn4.grid(row=3, column=0, padx=5, pady=5)

output_box = tk.Text(window, height=18, width=70, state="disabled")
output_box.pack(pady=10)

window.mainloop()
