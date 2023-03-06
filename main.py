from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

LABEL_FONT = ("Helvetica", 10, "normal")


def password_generator():
    if len(password_input.get()) < 1:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v',
                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                   'Q',
                   'R',
                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(4, 8)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        password_list = []
        password_list += [random.choice(letters) for _ in range(nr_letters)]
        password_list += [random.choice(numbers) for _ in range(nr_numbers)]
        password_list += [random.choice(symbols) for _ in range(nr_symbols)]
        random.shuffle(password_list)

        password = "".join(password_list)
        password_input.insert(0, string=password)
        pyperclip.copy(password)

    else:
        password_input.delete(0, END)
        password_generator()


def save():
    website_inputted = website_input.get().lower()
    username_inputted = username_input.get().lower()
    password_inputted = password_input.get().lower()
    new_pass_information = {
        website_inputted: {
            "email": username_inputted,
            "password": password_inputted
        }
    }

    if len(website_inputted) == 0 or len(password_inputted) == 0 or len(username_inputted) == 0:
        messagebox.showwarning(title="Warning", message="Fill all the fields.")
    else:
        if messagebox.askyesno(title="Confirm",
                               message=f"Do you want to save these data?\nWebsite: {website_inputted}\nEmail"
                                       f"/Username: {username_inputted}\nPassword: {password_inputted}"):
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
                    data.update(new_pass_information)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_pass_information, data_file, indent=4)
            else:
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                messagebox.showinfo(title="Saved", message="Your data is successfully saved.")
                website_input.delete(0, END)
                password_input.delete(0, END)
                website_input.focus()


def find_password():
    website_inputted = website_input.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            messagebox.showinfo(title="Search", message=f"Website: {website_inputted}\n"
                                                        f"Email/Username: {data[website_inputted]['email']}\n"
                                                        f"Password: {data[website_inputted]['password']}")
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="No saved data was found.")
    except KeyError:
        messagebox.showwarning(title="Warning", message=f"No data for '{website_input.get()}' was found.")
    else:
        website_input.delete(0, END)
        password_input.delete(0, END)
        website_input.focus()


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, background="white", highlightthickness=0)
image_file = PhotoImage(file="logo.png")
canvas.create_image(0, 0, image=image_file, anchor="nw")
canvas.grid(row=0, column=1)

""" Labels """
website_text = Label(text="Website:", anchor="center", background="white", font=LABEL_FONT)
website_text.grid(column=0, row=1)
website_text.config(pady=10)
emai_text = Label(text="Email/Username:", anchor="center", background="white", font=LABEL_FONT)
emai_text.grid(column=0, row=2)
emai_text.config(pady=10)
password_text = Label(text="Password:", anchor="center", background="white", font=LABEL_FONT)
password_text.grid(column=0, row=3)
password_text.config(pady=10)

""" Buttons """
generate_button = Button(text="Generate", width=9, font=LABEL_FONT, command=password_generator)
generate_button.grid(padx=5, column=2, row=3)
add_button = Button(text="Add", width=34, font=LABEL_FONT, command=save)
add_button.grid(padx=5, column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=9, font=LABEL_FONT, command=find_password)
search_button.grid(padx=5, row=1, column=2)

""" Inputs """
website_input = Entry(textvariable="", width=32)
website_input.grid(column=1, row=1)
website_input.focus()
username_input = Entry(textvariable="", width=46)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(0, "Your default email/Username")
password_input = Entry(textvariable="", width=32)
password_input.grid(column=1, row=3)

window.mainloop()
