import tkinter as tk
from PIL import Image, ImageTk
import random


with open("Assessment 1 - Skills Portfolio/A1 - Resources/randomJokes.txt", "r", encoding="utf-8") as f:
    raw_jokes = [line.strip() for line in f.readlines() if line.strip()]


jokes = []
for line in raw_jokes:
    if "?" in line:
        setup, punchline = line.split("?", 1)
        jokes.append((setup + "?", punchline))
    else:
        jokes.append((line, ""))

root = tk.Tk()
root.title("Joke Generator")
root.geometry("700x500")


root.resizable(True, True)



original_bg = Image.open("c:/Users/froms/OneDrive/Documents/GitHub/skills-portfolio-Sidharth13u/Assessment 1 - Skills Portfolio/joke/jok_bg.jpg")


bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1) 


def resize_bg(event):
    global bg_photo
    new_width = event.width
    new_height = event.height

   
    resized = original_bg.resize((new_width, new_height))
    bg_photo = ImageTk.PhotoImage(resized)

   
    bg_label.config(image=bg_photo)


root.bind("<Configure>", resize_bg)




setup_label = tk.Label(
    root,
    text="Click Alexa for a joke!",
    font=("Comic Sans MS", 16, "bold"),
    bg="yellow",
    fg="black",
    wraplength=500,
    justify="center",
    bd=5,
    relief="solid"
)
setup_label.place(relx=0.5, rely=0.40, anchor="center")

punchline_label = tk.Label(
    root,
    text="",
    font=("Comic Sans MS", 14, "bold"),
    bg="white",
    fg="red",
    wraplength=500,
    justify="center"
)
punchline_label.place(relx=0.5, rely=0.52, anchor="center")



button_style = {
    "font": ("Comic Sans MS", 14, "bold"),
    "bg": "#ffbf00",
    "fg": "black",
    "activebackground": "#ffdd55",
    "activeforeground": "black",
    "bd": 5,
    "relief": "ridge",
    "width": 16
}

current_setup = ""
current_punchline = ""

def alexa_joke():
    global current_setup, current_punchline
    current_setup, current_punchline = random.choice(jokes)
    setup_label.config(text=current_setup)
    punchline_label.config(text="")

def show_punchline():
    punchline_label.config(text=current_punchline)

def next_joke():
    alexa_joke()



alexa_button = tk.Button(root, text="Alexa tell me a Joke", command=alexa_joke, **button_style)
alexa_button.place(relx=0.5, rely=0.70, anchor="center")

punchline_button = tk.Button(root, text="Show Punchline", command=show_punchline, **button_style)
punchline_button.place(relx=0.5, rely=0.80, anchor="center")

next_button = tk.Button(root, text="NEXT JOKE", command=next_joke, **button_style)
next_button.place(relx=0.5, rely=0.90, anchor="center")

quit_button = tk.Button(root, text="QUIT", command=root.destroy, **button_style)
quit_button.place(relx=0.5, rely=0.97, anchor="center")

root.mainloop()