from tkinter import *
from tkinter import messagebox
import json
from random import randint, choice, shuffle
import pyperclip

FONT = ("Helvetica", 10)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()

    new_entry = {
        website: {
            "Email/Username": username,
            "Password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please fill all fields.")
    else:
        try:
            with open('data.json', 'r') as data_file:
                # Read old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                # Create new file
                json.dump(new_entry, data_file, indent=4)
        else:
            # Updating new data into old data
            data.update(new_entry)
            with open('data.json', 'w') as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


def search_password():
    website = website_input.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No file is found.")
    else:
        if website in data:
            username = data[website]["Email/Username"]
            password = data[website]["Password"]
            pyperclip.copy(password)
            messagebox.showinfo(title=website, message=f"Username/Email: {username}\nPassword '{password}' is copied!")
        else:
            messagebox.showinfo(title="Error", message=f"Password for {website} not found.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Jenny's Password Manager")
window.config(padx=50, pady=50)

# set up logo
canvas = Canvas(window, width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# set up website input
website_label = Label(text="Website:", font=FONT)
website_label.grid(column=0, row=1)
website_input = Entry(width=33)
website_input.grid(column=1, row=1)
website_input.focus()

# set up search button
search_button = Button(text="Search Password", font=FONT, command=search_password, width=14)
search_button.grid(column=2, row=1)

# set up email/username input
username_label = Label(text="Email/Username:", font=FONT)
username_label.grid(column=0, row=2)
username_input = Entry(width=54)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(0, "zhuzhi7@gmail.com")

# set up password input
password_label = Label(text="Password:", font=FONT)
password_label.grid(column=0, row=3)
password_input = Entry(width=33)
password_input.grid(column=1, row=3)

#set up buttons
password_gen_button = Button(text="Generate Password", font=FONT, command=generate_password)
password_gen_button.grid(column=2, row=3)

add_button = Button(text="Add", font=FONT, width=40, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
