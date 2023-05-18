import tkinter as tk
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

#--------------------CARDS & DATA SETUP----------------------#

current_word = {}
to_learn = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=canvas_old)
    flip_timer = window.after(3000, func=flip_cards)

def flip_cards():
    canvas.itemconfig(canvas_image, image=canvas_new)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_word["English"], fill="white")

def is_known():
    to_learn.remove(current_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

#---------------------UI SETUP-----------------------#

window = tk.Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.geometry("900x702")
window.title("Flash Card")

flip_timer = window.after(3000, func=flip_cards)

canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_old = PhotoImage(file="images/card_front.png")
canvas_new = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(410, 263, image=canvas_old)

#conviene crear variables de lo que se pueda llegar a modificar después a través de funciones
word = canvas.create_text(400, 300, text="word", fill="black", font=("Courier", 35, "bold"))
title = canvas.create_text(400, 190, text="French", fill="black", font=("Courier", 26, "italic"))

canvas.grid(columnspan=2)

cross_button_image = PhotoImage(file="images/wrong.png")
cross_button = tk.Button(image=cross_button_image, highlightthickness=0, command=next_card)
cross_button.grid(column=0, row=2)
check_button_image = PhotoImage(file="images/right.png")
check_button = tk.Button(image=check_button_image, highlightthickness=0, command=is_known)
check_button.grid(column=1, row=2)

next_card()

window.mainloop()
