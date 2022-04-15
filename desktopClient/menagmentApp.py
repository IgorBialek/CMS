import tkinter as tk
from tkinter import ttk
import tkinter
from turtle import right
from ttkthemes import ThemedTk
from tksheet import Sheet
import pymongo
import re


# from tkinter.ttk import Notebook

window = ThemedTk(theme="breeze")
window.geometry("900x500")
window.title("Menagment")
window.configure(bg='#3dade9')


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["cms"]
db_collection_users = db["users"]

try:
    db_collection_users.insert_one({ "_id": "admin", "password": "admin", "permission": "admin"})
except Exception as exception:
    print("Admin already exists")

users = db_collection_users.find({}, {})



notebookSections = ttk.Notebook(window)
notebookSections.pack(anchor='center', expand=True, pady=10)


frames = {}
Users = ttk.Frame(notebookSections, width=600, height=300)


# choosedUserLogin = ""
# choosedUserPassword = ""

def load_data_to_sheet():
    global db_collection_users
    sheet.set_sheet_data([[user["_id"], user["password"], user["permission"]] for user in db_collection_users.find({}, {})])


def insert_user(email, password, permission):
    global typeOfSaving
    global db_collection_users
    global editedUserId

    if typeOfSaving == "edit":
        db_collection_users.delete_one({ "_id": editedUserId})

    db_collection_users.insert_one({ "_id": email, "password": password, "permission": permission })

    load_data_to_sheet()


def delete_user():
    global sheet
    global db_collection_users

    try:
        sheetData = next(iter(sheet.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))  
        db_collection_users.delete_one({"_id": sheet.get_row_data(sheetData, return_copy = True)[0], "password": sheet.get_row_data(sheetData, return_copy = True)[1], "permission": sheet.get_row_data(sheetData, return_copy = True)[2]})
        sheet.deselect(row = sheetData, column = None, cell = None, redraw = True)
        load_data_to_sheet()
    except Exception as exception:
        tk.messagebox.showinfo("showinfo", "User is not selected, you have to click on the number of row")

def show_users_or_edit_content(page_name, type):
    global Users
    global frames
    global notebookSections
    global passwordRepeatEntry
    global passwordEntry
    global emailEntry
    global permissionCombobox
    global sheet
    global users
    global typeOfSaving
    global editedUserId
    '''Show a frame for the given page name'''

    emailIsValid = True
    passwordIsValid = True



    if page_name == "UsersEdit":
        emailEntry.delete(0, 'end')
        passwordEntry.delete(0, 'end')
        passwordRepeatEntry.delete(0, 'end')       

    if type == "edit":
        try:
            sheetData = next(iter(sheet.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))  
            emailEntry.insert(0, sheet.get_row_data(sheetData, return_copy = True)[0])
            passwordEntry.insert(0, sheet.get_row_data(sheetData, return_copy = True)[1])
            passwordRepeatEntry.insert(0, sheet.get_row_data(sheetData, return_copy = True)[1])
            permissionCombobox.set( sheet.get_row_data(sheetData, return_copy = True)[2])
            typeOfSaving = "edit"
            editedUserId = sheet.get_row_data(sheetData, return_copy = True)[0]
        except Exception as exception:
            print("User is not selected")
            tk.messagebox.showinfo("showinfo", "User is not selected, you have to click on the number of row")
            return
    elif type == "add":
            typeOfSaving = "add"
            permissionCombobox.set("user")
    elif type == "save":
        emailIsValid = emailEntry.validate()
        passwordIsValid = passwordRepeatEntry.validate()

        if emailIsValid and passwordIsValid:
            insert_user(emailEntry.get(), passwordEntry.get(), permissionCombobox.get())


    if emailIsValid and passwordIsValid:
        for frame in frames.keys():
            if frame == page_name:
                frames[frame].pack()
            else:
                frames[frame].pack_forget()


def check_email():
    global emailEntry
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    if re.search(regex, emailEntry.get()):
        infoLabel.config(text="")
        return True
    else:
        infoLabel.config(text="Email is not valid")
        return False


def check_passwords():
    global passwordEntry
    global passwordRepeatEntry

    if len(passwordEntry.get()) > 0 and len(passwordRepeatEntry.get()) > 0 and passwordRepeatEntry.get() == passwordEntry.get():
        infoLabel.config(text="")
        return True
    else:
        infoLabel.config(text="Passwords must be equal and cannot be empty")
        return False


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

deleteBtn = ttk.Button(UsersButtonsFrame, text="Delete", command= lambda: delete_user())
deleteBtn.pack(side="left", pady=10, padx=5)



sheet = Sheet(UsersDefault, width=570, enable_edit_cell_auto_resize = False)
sheet.pack()

sheet.headers(newheaders = ["email", "password", "permission"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
#RAZ TRZEBA () A RAZ (()), NIE WIEM CZEMU
load_data_to_sheet()
sheet.enable_bindings(("row_select","single_select"))




#USER EDIT
UsersButtonsFrameEdit = ttk.Frame(UsersEdit, width=600)
UsersButtonsFrameEdit.pack()
cancelBtn = ttk.Button(UsersButtonsFrameEdit, text="Cancel", command= lambda: show_users_or_edit_content("UsersDefault", "cancel"))
cancelBtn.pack(side="left", pady=10, padx=5)

InfoUserEditFrame = ttk.Frame(UsersEdit, width=600)
InfoUserEditFrame.pack(side="bottom")
infoLabel = ttk.Label(InfoUserEditFrame, text="")
infoLabel.pack()

typeOfSaving = ""
editedUserId = ""
SaveButtonFrame = ttk.Frame(UsersEdit, width=600)
SaveButtonFrame.pack(side="bottom")
saveBtn = ttk.Button(SaveButtonFrame, text="Save", command= lambda: show_users_or_edit_content("UsersDefault", "save"))
saveBtn.pack(side="left", pady=10, padx=5)


PermissionFrame = ttk.Frame(UsersEdit, width=300)
PermissionFrame.pack(side="bottom")
permissionLabel = ttk.Label(PermissionFrame, text="Permission", width=15)
permissionLabel.pack(side="left")
selected_role = tk.StringVar()
permissionCombobox = ttk.Combobox(PermissionFrame, textvariable=selected_role, width=24, state = "readonly")
permissionCombobox['values'] = ["admin", "permitted", "user"]
permissionCombobox.pack(side="right")


PasswordRepeatFrame = ttk.Frame(UsersEdit, width=300)
PasswordRepeatFrame.pack(side="bottom")
passwordRepeatLabel = ttk.Label(PasswordRepeatFrame, text="Password repeat", width=15)
passwordRepeatLabel.pack(side="left")
passwordRepeatEntry = ttk.Entry(PasswordRepeatFrame, width=25)
passwordRepeatEntry.pack(side="right")
passwordRepeatEntry.config(validate="focusout", validatecommand=check_passwords)
#passwordRepeatEntry.insert(0, choosedUserPassword)

PasswordFrame = ttk.Frame(UsersEdit, width=300)
PasswordFrame.pack(side="bottom")
passwordLabel = ttk.Label(PasswordFrame, text="Password", width=15)
passwordLabel.pack(side="left")
passwordEntry = ttk.Entry(PasswordFrame, width=25)
passwordEntry.pack(side="right")
#passwordEntry.insert(0, choosedUserPassword)

UsersEmailFrame = ttk.Frame(UsersEdit, width=300)
UsersEmailFrame.pack(side="bottom")
emailLabel = ttk.Label(UsersEmailFrame, text="Email", width=15)
emailLabel.pack(side="left")
emailEntry = ttk.Entry(UsersEmailFrame, width=25 )
emailEntry.config(validate="focusout", validatecommand=check_email)
emailEntry.pack(side="right")



#emailEntry.insert(0, choosedUserLogin)



window.mainloop()