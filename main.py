from tkinter import *
from PIL import Image, ImageTk
import sys, os, pandas, json

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 24, "italic")
WORD_FONT = ("Ariel", 46, "bold")
flip_timer = 0
current_word = {}

# ---------------------- GENERATE NEW WORDS ------------------------- #

dict_data = pandas.read_csv("./data/french_words.csv")


# french_dict = {row.French:row.English for (index, row) in dict_data.iterrows()} # example: {"partie": "party"}
# french_dict = pandas.DataFrame.to_dict(dict_data, orient="records")

# def get_random_word_method_1():
#     random_french_word, random_english_word = random.choice(list(french_dict.items()))
#     return random_french_word, random_english_word
#     random_word = pandas.DataFrame.sample(dict_data)
#     random_french_word, random_english_word = pandas.Series.tolist(random_word)[0]
#     return random_french_word, random_english_word


# def get_random_word_method_2():
#     ran_num = random.randint(0, len(dict_data.index)-1)
#     random_french_word, random_english_translation = dict_data.French[ran_num], dict_data.English[ran_num]
#     return random_french_word, random_english_translation

def get_random_word():
    random_word_series = pandas.DataFrame.sample(dict_data)
    return {
        "French": random_word_series.French.values[0],
        "English": random_word_series.English.values[0]
    }


# ------------------------- SAVE WORD TO REVIEW IN JSON --------------------------- #

# def save_word_for_review():
#     global current_word
#     print("Current word is:", current_word)
#     word_to_review = {current_word["French"]:current_word["English"]}
#     print("Word to review is:", word_to_review)
#
#     try:
#         with open("./words_to_review.json", 'r') as file:
#             log_data = json.load(file)
#             print("Loaded log Data:", log_data)
#
#     except FileNotFoundError:
#         log_data = {}
#         print("file not found")
#
#     # else:
#     #     log_data.update(word_to_review)
#     #     print("Updated log Data:", log_data)
#
#     finally:
#         log_data.update(word_to_review)
#         print("Updated log Data:", log_data)
#         with open("./words_to_review.json", 'w') as file:
#             json.dump(log_data, file, indent=4)
#             print("Word to review saved")


# ------------------- SAVE WORD TO REVIEW IN CSV ---------------------- #

def save_word_for_review():
    """import current, open CSV and append to CSV"""
    global current_word
    word_to_review = {
        "French": [current_word["French"]],
        "English": [current_word["English"]]
    }
    word_to_review_row = pandas.DataFrame(word_to_review)
    try:
        data_words = pandas.read_csv("./words_to_review.csv")
        # Remove the index ('unnamed') column from the working data file
        # data_words = data_words.loc[:, ~data_words.columns.str.contains('^Unnamed')]
        # if data_words.loc[(data_words.French == current_word["French"]) & (data_words.English == current_word["English"])].shape[0] > 0:
        # if not df[(df['Name'] == 'John Smith') & (df['Age'] == 35)].empty:
        #     print("Already exists")

    except FileNotFoundError:
        word_to_review_row.to_csv("./words_to_review.csv", index=False)
        print("New file created")
    else:
        row_exists = ((data_words["French"] == current_word["French"]) & (data_words["English"] == current_word["English"])).any()
        if row_exists:
            print("Already exists")
        else:
            updated_data = pandas.concat([data_words, word_to_review_row], ignore_index=True)
            updated_data.to_csv("./words_to_review.csv", index=False)
            print(updated_data)


# ---------------------------- UI SETUP ------------------------------- #

# WINDOW
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50)
window.config(background=BACKGROUND_COLOR)
window.resizable(height=True, width=True)


# CARD
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Load front card
front_card_pillow_img = Image.open(resource_path("./images/card_front.png"))  # import with PIL to get image dimensions
resized_front_card_img = front_card_pillow_img.resize((600, 400), resample=Image.LANCZOS)
front_card_tkimg = ImageTk.PhotoImage(resized_front_card_img)  # format to PhotoImage

# Load back card
back_card_pillow_img = Image.open(resource_path("./images/card_back.png"))
resized_back_card_img = back_card_pillow_img.resize((600, 400), resample=Image.LANCZOS)
back_card_tkimg = ImageTk.PhotoImage(resized_back_card_img)

card = Canvas(width=front_card_tkimg.width(), height=front_card_tkimg.height(), highlightthickness=0,
              bg=BACKGROUND_COLOR)
canvas_background = card.create_image(0, 0, image=front_card_tkimg, anchor=NW)
card.grid(row=0, column=0, columnspan=2)


# FRONT CARD

def find_center():
    window.update()  # must update tkinter before winfo_width
    canvas_width, canvas_height = card.winfo_width(), card.winfo_height()
    x_offset, y_offset = canvas_width / 2, canvas_height / 2
    return x_offset, y_offset


# Language bar
language_text = card.create_text(find_center()[0], find_center()[1] * (1 / 2), font=LANGUAGE_FONT, text="French")

# Word bar
current_word = get_random_word()
print("Pre loaded current word is: ", current_word)
word_text = card.create_text(find_center()[0], find_center()[1], font=WORD_FONT, text=current_word["French"])

# Generate New Word on Front Card
# def next_word():
#     global current_word, flip_timer
#     window.after_cancel(flip_timer)
#     current_word = get_random_word()
#     card.itemconfigure(word_text, text=current_word["French"], fill="black")
#     card.itemconfigure(language_text, text="French", fill="black")
#     card.itemconfigure(canvas_background, image=front_card_tkimg)
#     flip_timer = window.after(3000, func=flip_card)
#
#
# def flip_card():
#     """After 3 seconds, flip the card and show English translation"""
#     # Change to back of the card
#     card.itemconfigure(canvas_background, image=back_card_tkimg)
#
#     # Show English translation and font to white
#     card.itemconfigure(word_text, text=current_word["English"], fill="white")
#
#     # Change language text to "English" and font to white
#     card.itemconfigure(language_text, text="English", fill="white")


"""Alternative solutions"""


def flip_card(current_word):
    # Change to back of the card
    card.itemconfigure(canvas_background, image=back_card_tkimg)

    # Show English translation and font to white
    card.itemconfigure(word_text, text=current_word["English"], fill="white")

    # Change language text to "English" and font to white
    card.itemconfigure(language_text, text="English", fill="white")


def next_word():
    global flip_timer, current_word
    window.after_cancel(flip_timer)
    current_word = get_random_word()
    print("Next Word current word is:", current_word)
    card.itemconfigure(word_text, text=current_word["French"], fill="black")
    card.itemconfigure(language_text, text="French", fill="black")
    card.itemconfigure(canvas_background, image=front_card_tkimg)
    flip_timer = window.after(3000, flip_card, current_word)


# RED WRONG BUTTON
red_button_pillow_img = Image.open(resource_path("./images/wrong.png"))
red_button_tkimg = ImageTk.PhotoImage(red_button_pillow_img)
red_button_widget = Button(image=red_button_tkimg, bg=BACKGROUND_COLOR, relief="flat",
                           command=lambda: [save_word_for_review(), next_word()])
red_button_widget.grid(row=1, column=0)

# GREEN CORRECT BUTTON
green_button_pillow_img = Image.open(resource_path("./images/right.png"))
green_button_tkimg = ImageTk.PhotoImage(green_button_pillow_img)
green_button_widget = Button(image=green_button_tkimg, bg=BACKGROUND_COLOR, relief="flat", command=next_word)
green_button_widget.grid(row=1, column=1)

# flip_timer = window.after(3000, func=flip_card)
flip_timer = window.after(3000, flip_card, current_word)

# CLOSE APP
window.mainloop()
