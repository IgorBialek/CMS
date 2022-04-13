import tkinter as tk
from tkinter import ttk
from turtle import right
from ttkthemes import ThemedTk
from tksheet import Sheet
import pymongo

# from tkinter.ttk import Notebook

window = ThemedTk(theme="breeze")
window.geometry("900x500")
window.title("Menagment")
window.configure(bg='#3dade9')


notebookSections = ttk.Notebook(window)
notebookSections.pack(anchor='center', expand=True, pady=10)


frames = {}
Users = ttk.Frame(notebookSections, width=600, height=300)


choosedUserLogin = ""
choosedUserPassword = ""


def show_users_or_edit_content(page_name, type):
    global Users
    global frames
    global notebookSections
    global choosedUserLogin, choosedUserPassword
    '''Show a frame for the given page name'''
    print
    print(frames[page_name])
    print(frames.keys())
    print(page_name)

    if(type == "add"):
        choosedUserLogin = "ddd"
        choosedUserPassword = "ddd"

    for frame in frames.keys():
        if frame == page_name:
            frames[frame].pack()
        else:
            frames[frame].pack_forget()





UsersEdit = ttk.Frame(Users, width=600, height=300)
UsersEdit.pack(side="left")

UsersDefault = ttk.Frame(Users, width=600, height=300)
UsersDefault.pack(side="left")

frames = {"UsersDefault": UsersDefault, "UsersEdit": UsersEdit}

#ustawienie wyswietlania
show_users_or_edit_content("UsersDefault", "")



#MAIN WORK
Navbar = ttk.Frame(notebookSections, width=600, height=300)
News = ttk.Frame(notebookSections, width=600, height=300)
Footer = ttk.Frame(notebookSections, width=600, height=300)
Slider = ttk.Frame(notebookSections, width=600, height=300)

notebookSections.add(Users, text="Users")
notebookSections.add(Navbar, text="Navbar")
notebookSections.add(News, text="News")
notebookSections.add(Footer, text="Footer")
notebookSections.add(Slider, text="Slider")



#USER DEFAULT
UsersButtonsFrame = ttk.Frame(UsersDefault, width=600)
UsersButtonsFrame.pack()

addBtn = ttk.Button(UsersButtonsFrame, text="Add", command= lambda: show_users_or_edit_content("UsersEdit", "add"))
addBtn.pack(side="left", pady=10, padx=5)

editBtn = ttk.Button(UsersButtonsFrame, text="Edit" , command= lambda: show_users_or_edit_content("UsersEdit", "edit"))
editBtn.pack(side="left", pady=10, padx=5)

deleteBtn = ttk.Button(UsersButtonsFrame, text="Delete")
deleteBtn.pack(side="left", pady=10, padx=5)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["cms"]
db_collection_users = db["users"]

users = db_collection_users.find({}, {})
print(users)

sheet = Sheet(UsersDefault, width=570, enable_edit_cell_auto_resize = False)
sheet.pack()

sheet.headers(newheaders = ["email", "password", "permission"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
sheet.set_sheet_data([[user["_id"], user["_id"], user["_id"]] for user in users])
sheet.enable_bindings("row_select","single_select")




#USER EDIT
UsersButtonsFrameEdit = ttk.Frame(UsersEdit, width=600)
UsersButtonsFrameEdit.pack()
cancelBtn = ttk.Button(UsersButtonsFrameEdit, text="Cancel", command= lambda: show_users_or_edit_content("UsersDefault"))
cancelBtn.pack(side="left", pady=10, padx=5)



PasswordRepeatFrame = ttk.Frame(UsersEdit, width=300)
PasswordRepeatFrame.pack(side="bottom")
passwordRepeatLabel = ttk.Label(PasswordRepeatFrame, text="Password repeat", width=15)
passwordRepeatLabel.pack(side="left")
passwordRepeatEntry = ttk.Entry(PasswordRepeatFrame, width=25)
passwordRepeatEntry.pack(side="right")
passwordRepeatEntry.insert(0, choosedUserPassword)

PasswordFrame = ttk.Frame(UsersEdit, width=300)
PasswordFrame.pack(side="bottom")
passwordLabel = ttk.Label(PasswordFrame, text="Password", width=15)
passwordLabel.pack(side="left")
passwordEntry = ttk.Entry(PasswordFrame, width=25)
passwordEntry.pack(side="right")
passwordEntry.insert(0, choosedUserPassword)

UsersEmailFrame = ttk.Frame(UsersEdit, width=300)
UsersEmailFrame.pack(side="bottom")
emailLabel = ttk.Label(UsersEmailFrame, text="Email", width=15)
emailLabel.pack(side="left")
emailEntry = ttk.Entry(UsersEmailFrame, width=25)
emailEntry.pack(side="left")
emailEntry.insert(0, choosedUserLogin)



window.mainloop()