import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")





# ---------------------------- RANDOM GENERATION ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- TIMER ------------------------------- #
def flip_card():
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_text, fill="white", text=current_card["English"])


def know_answer():
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", fill="black", font=("Ariel", 28, "italic"))
card_text = canvas.create_text(400, 263, text="word", fill="black", font=("Ariel", 35, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

yes_button_img = PhotoImage(file="images/right.png")
no_button_img = PhotoImage(file="images/wrong.png")

yes_button = Button(image=yes_button_img, highlightthickness=0, command=know_answer)
yes_button.grid(column=1, row=1)

no_button = Button(image=no_button_img, highlightthickness=0, command=next_card)
no_button.grid(column=0, row=1)

next_card()

window.mainloop()
