import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

def check_answer():
    global score, current_question_index, timer_running

    try:
        user_ans = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a valid number!")
        return   # <-- Do NOT stop timer, just return

    # Stop timer only when valid answer given
    timer_running = False

    correct_total = questions[current_question_index]["answer"]

    if user_ans == correct_total:
        if not questions[current_question_index]["answered"]:
            score += 10
        questions[current_question_index]["answered"] = True

        messagebox.showinfo("Nice!", f"✅ Correct! The total was ${correct_total}")
    else:
        messagebox.showwarning("Wrong", "❌ Wrong answer!")

    go_next()


# -------------------- MENU DATA --------------------
snacks = ["Croissant", "Muffin", "Sandwich", "Donut", "Brownie", "Cake Slice", "Bagel", "Cookie"]
drinks = ["Coffee", "Tea", "Orange Juice", "Milkshake", "Hot Chocolate", "Smoothie", "Lemonade", "Iced Coffee"]

timer_label = None
time_left = 10
timer_running = False
timer_id = None   # <<< added

# -------------------- BACKGROUND FUNCTION --------------------
def set_background():
    global bg_label, bg_photo
    bg_img = Image.open(r"C:\Users\froms\Downloads\web3\skills-portfolio-Sidharth13u\Assessment 1 - Skills Portfolio\cafe.png")
    bg_img = bg_img.resize((1920, 1080))
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# -------------------- TIMER --------------------
def start_timer():
    global time_left, timer_running, timer_id

    # cancel old timer if running
    if timer_id:
        root.after_cancel(timer_id)

    time_left = 10
    timer_running = True
    update_timer()

def update_timer():
    global time_left, timer_running, timer_id

    if not timer_running:
        return

    if timer_label:
        timer_label.config(text=f"⏳ Time Left: {time_left}s")

    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, update_timer)
    else:
        timer_running = False
        messagebox.showwarning("Time Up!", "⏰ Time has expired!")
        go_next(auto=True)

# -------------------- FUNCTIONS --------------------
def displayMenu():
    clear_window()

    tk.Label(root, text="☕ Café Bill Calculator ☕", font=("Arial", 30, "bold"),
             fg="#3e2723", bg="#ffffff").pack(pady=30)

    tk.Label(root, text="SELECT DIFFICULTY LEVEL", font=("Arial", 22, "bold"),
             bg="#ffffff").pack(pady=20)

    tk.Button(root, text="1. Easy (Cheap Café)", font=("Arial", 18), width=30,
              command=lambda: start_quiz("Easy")).pack(pady=15)
    tk.Button(root, text="2. Moderate (Standard Café)", font=("Arial", 18), width=30,
              command=lambda: start_quiz("Moderate")).pack(pady=15)
    tk.Button(root, text="3. Advanced (Luxury Café)", font=("Arial", 18), width=30,
              command=lambda: start_quiz("Advanced")).pack(pady=15)

    tk.Label(root, text="You’ll be calculating total bills for 10 café orders.",
             font=("Arial", 16), fg="gray", bg="#ffffff").pack(pady=15)

def priceRange(level):
    if level == "Easy":
        return 1, 10
    elif level == "Moderate":
        return 10, 50
    else:
        return 50, 200

def displayProblem():
    global timer_label

    clear_window()
    q_data = questions[current_question_index]
    question = q_data["question"]

    tk.Label(root, text=f"Order {current_question_index + 1}/10",
             font=("Arial", 20, "italic"), bg="#ffffff").pack(pady=10)

    tk.Label(root, text="🍩 Cozy Café Counter 🍪",
             font=("Arial", 26, "bold"), fg="#4e342e", bg="#ffffff").pack(pady=10)

    tk.Label(root, text=question, font=("Arial", 28, "bold"), bg="#ffffff").pack(pady=40)

    global answer_entry
    answer_entry = tk.Entry(root, font=("Arial", 24))
    answer_entry.pack(pady=20)
    answer_entry.focus()

    timer_label = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="#ffffff", fg="red")
    timer_label.pack()

    start_timer()

    btn_frame = tk.Frame(root, bg="#ffffff")
    btn_frame.pack(pady=40)

    if current_question_index == 0:
        tk.Button(btn_frame, text="Back", font=("Arial", 18),
                  command=lambda: go_next(back_to_menu=True)).grid(row=0, column=0, padx=20)
    else:
        tk.Button(btn_frame, text="Previous", font=("Arial", 18),
                  command=go_previous).grid(row=0, column=0, padx=20)

    if current_question_index == 9:
        tk.Button(btn_frame, text="Submit Quiz", font=("Arial", 18),
                  command=check_answer).grid(row=0, column=1, padx=20)
    else:
        tk.Button(btn_frame, text="Next", font=("Arial", 18),
                  command=check_answer).grid(row=0, column=1, padx=20)

def check_answer():
    global score, current_question_index, timer_running
    timer_running = False

    try:
        user_ans = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a valid number!")
        return

    correct_total = questions[current_question_index]["answer"]

    if user_ans == correct_total:
        if not questions[current_question_index]["answered"]:
            score += 10
        questions[current_question_index]["answered"] = True

        messagebox.showinfo("Nice!", f"✅ Correct! The total was ${correct_total}")
    else:
        messagebox.showwarning("Wrong", "❌ Wrong answer!")

    go_next()

def go_next(auto=False, back_to_menu=False):
    global current_question_index

    if back_to_menu:
        displayMenu()
        return

    if current_question_index < 9:
        current_question_index += 1
        displayProblem()
    else:
        displayResults()

def go_previous():
    global current_question_index, timer_running

    timer_running = False

    if current_question_index > 0:
        current_question_index -= 1
        displayProblem()

def displayResults():
    clear_window()

    tk.Label(root, text="🍰 Café Summary 🍰", font=("Arial", 36, "bold"),
             fg="#3e2723", bg="#ffffff").pack(pady=40)
    tk.Label(root, text=f"Your Final Score: {score}/100",
             font=("Arial", 28, "bold"), bg="#ffffff").pack(pady=20)

    if score >= 90:
        rank = "Master Barista ☕"
    elif score >= 70:
        rank = "Skilled Cashier 🧾"
    elif score >= 50:
        rank = "Trainee 🍪"
    else:
        rank = "Needs Practice 🍩"

    tk.Label(root, text=f"Your Rank: {rank}", font=("Arial", 26), bg="#ffffff").pack(pady=25)

    tk.Button(root, text="Play Again", font=("Arial", 22), command=displayMenu).pack(pady=15)
    tk.Button(root, text="Exit", font=("Arial", 22), command=root.destroy).pack(pady=15)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()
    set_background()

def start_quiz(selected_level):
    global level, score, current_question_index, questions
    level = selected_level
    score = 0
    current_question_index = 0
    questions = []
    ops = ["+"] * 5 + ["-"] * 5
    random.shuffle(ops)

    min_p, max_p = priceRange(level)

    for op in ops:
        snack = random.choice(snacks)
        drink = random.choice(drinks)
        s_price = random.randint(min_p, max_p)
        d_price = random.randint(min_p, max_p)

        if op == "+":
            q = f"{snack} (${s_price}) + {drink} (${d_price}) = ?"
            ans = s_price + d_price
        else:
            q = f"{snack} (${s_price}) - {drink} (${d_price}) = ?"
            ans = s_price - d_price

        questions.append({"question": q, "answer": ans, "answered": False})

    displayProblem()

# -------------------- MAIN GUI --------------------
root = tk.Tk()
root.title("Café Bill Calculator Quiz")
root.state("zoomed")

set_background()
displayMenu()

root.protocol("WM_DELETE_WINDOW", root.destroy)


root.mainloop()
