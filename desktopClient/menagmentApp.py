from cgitb import text
from glob import glob
from math import fabs
import tkinter as tk
from tkinter import ttk
from traceback import print_tb
from turtle import bgcolor, width
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


def show_users_or_edit_content(page_name):
    global Users
    global frames
    global notebookSections
    '''Show a frame for the given page name'''
    print
    print(frames[page_name])
    print(frames.keys())
    print(page_name)

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
UsersButtonsFrame = ttk.Frame(UsersDefault, width=600)
UsersButtonsFrame.pack()
#ustawienie wyswietlania
show_users_or_edit_content("UsersDefault")


Navbar = ttk.Frame(notebookSections, width=600, height=300)
News = ttk.Frame(notebookSections, width=600, height=300)
Footer = ttk.Frame(notebookSections, width=600, height=300)
Slider = ttk.Frame(notebookSections, width=600, height=300)


# title = Label(window, text="Menagment app")
# title.pack()
notebookSections.add(Users, text="Users")
notebookSections.add(Navbar, text="Navbar")
notebookSections.add(News, text="News")
notebookSections.add(Footer, text="Footer")
notebookSections.add(Slider, text="Slider")


addBtn = ttk.Button(UsersButtonsFrame, text="Add", command= lambda: show_users_or_edit_content("UsersEdit"))
addBtn.pack(side="left", pady=10, padx=5)

editBtn = ttk.Button(UsersButtonsFrame, text="Edit")
editBtn.pack(side="left", pady=10, padx=5)

deleteBtn = ttk.Button(UsersButtonsFrame, text="Delete")
deleteBtn.pack(side="left", pady=10, padx=5)


testLabel = ttk.Label(UsersEdit, text="inny content")
testLabel.pack()


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["cms"]
db_collection_users = db["users"]

users = db_collection_users.find({}, {})
print(users)

sheet = Sheet(UsersDefault, width=570, enable_edit_cell_auto_resize = False)
sheet.pack()


def new_right_click_button(event = None):
    print ("Hello World!")

sheet.headers(newheaders = ["email", "password", "permission"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
sheet.set_sheet_data([[user["_id"], user["_id"], user["_id"]] for user in users])
sheet.enable_bindings(("row_select", "single_select"))
sheet.popup_menu_add_command("Say Hello", new_right_click_button)



window.mainloop()
