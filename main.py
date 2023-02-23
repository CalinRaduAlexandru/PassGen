from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(6, 8))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

def search_database():
    try:
        with open("data.json", "r") as data_file:
            website = website_entry.get().lower()
            if len(website) > 0:
                data = json.load(data_file)
                if website in data:
                    messagebox.showinfo(title="success", message=f"Website: {website} \n "
                                                                 f"Email: {data[website]['email']} \n "
                                                                 f"Password: {data[website]['password']} ")
                else:
                    messagebox.showinfo(title="didnt find", message=f"This '{website}' website information couldn't be found.")
            else:
                messagebox.showinfo(title="Oops", message="Please make sure you haven't left website field empty.")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="There is no info to show")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
        "email" : email,
        "password" : password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nWebsite: {website} \n  Email: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)


            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)


#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=20)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=37)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "radu@gmail.com")
password_entry = Entry(width=20)
password_entry.grid(row=3, column=1)

generate_password()

# Button - Search data
generate_password_button = Button(text="Search", width=14, command=search_database)
generate_password_button.grid(row=1, column=2)

# Button - Generate password
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

# Button - Add DATA
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()