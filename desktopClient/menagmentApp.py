import enum
from msilib.schema import Component
from operator import index
import tkinter as tk
from tkinter import ttk
import tkinter
from turtle import right, title
from ttkthemes import ThemedTk
from tksheet import Sheet
import pymongo
import re
import ctypes
import os

myappid = 'appIcon.ico' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


# from tkinter.ttk import Notebook

window = ThemedTk(theme="breeze")
window.geometry("900x500")
window.title("Menagment")
window.configure(bg='#3dade9')

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
window.iconbitmap(os.path.join(__location__, 'appIcon.ico'))


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["cms"]
db_collection_users = db["users"]
db_collection_pageConfiguration = db["pageConfiguration"]


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

def on_tab_change(event):
    global notebookSections
    tab = event.widget.tab('current')['text']
    print(tab)

    if tab == "Users":
        load_data_to_sheet()
        pass
    elif tab == "Navbar":
        load_data_to_navbar_section()
    elif tab == "News":
        load_data_to_news_sheet()
    elif tab == "Footer":
        load_data_to_footer_section()
    elif tab == "Slider":
        load_data_to_slider_sheet()


def load_data_to_sheet():
    global db_collection_users
    global sheet


    try:
        sheet.set_sheet_data([[user["_id"], user["password"], user["permission"]] for user in db_collection_users.find({}, {})])
    except:
        print("Page is laoding")


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
UsersDefault.pack(side="left", padx=5)

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

notebookSections.bind('<<NotebookTabChanged>>', on_tab_change)



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
sheet.enable_bindings(("row_select","single_select"))
load_data_to_sheet()



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

#########################################################################################################
entriesArticles = []


def load_data_to_navbar_section():

    global rowIndexNavbar
    global selectedTemplate
    #global dataPageConfigurationNavbarArticles

    for widget in Navbar.winfo_children():
        widget.destroy()

    Navbar.columnconfigure(0, weight=1)
    Navbar.columnconfigure(1, weight=1)
    Navbar.columnconfigure(2, weight=1)

    navbarColumnHeaderTitleLabel = ttk.Label(Navbar, text="Title")
    navbarColumnHeaderTitleLabel.grid(column=0, row=0, padx=5, pady=5)
    navbarColumnHeaderTextLabel = ttk.Label(Navbar, text="Text")
    navbarColumnHeaderTextLabel.grid(column=1, row=0, padx=5, pady=5)
    navbarColumnHeaderLinkLabel = ttk.Label(Navbar, text="Link")
    navbarColumnHeaderLinkLabel.grid(column=2, row=0, padx=5, pady=5)

    print(type(db_collection_pageConfiguration.find({}, {})))

    dataPageConfigurationNavbar = db_collection_pageConfiguration.find({}, {})
    selectedTemplate = dataPageConfigurationNavbar[0]["configuration"]["selectedTemplate"]
    dataPageConfigurationNavbarArticles = dataPageConfigurationNavbar[0]["configuration"]["templates"][selectedTemplate]["menu"]["articles"]


    rowIndexNavbar = 0

    for i,article in enumerate(dataPageConfigurationNavbarArticles):
        print(article['title'])
        articleEntryTitle = ttk.Entry(Navbar)
        articleEntryTitle.grid(column=0, row=i + 1, padx=5, pady=5)
        articleEntryTitle.insert(0, article["title"])
        articleEntryText = ttk.Entry(Navbar)
        articleEntryText.grid(column=1, row=i + 1, padx=5, pady=5)
        articleEntryText.insert(0, article["text"])
        articleEntryLink = ttk.Entry(Navbar)
        articleEntryLink.grid(column=2, row=i + 1, padx=5, pady=5)
        articleEntryLink.insert(0, article["link"])
        rowIndexNavbar = i + 1
        entriesArticles.append([articleEntryTitle, articleEntryText, articleEntryLink])

    rowIndexNavbar += 1

    saveArticlesNavbar = ttk.Button(Navbar, text="Save", command=save_articles)
    saveArticlesNavbar.grid(column=1, row=rowIndexNavbar, padx=5, pady=5)


def save_articles():   
    global rowIndexNavbar
    global selectedTemplate
    # print(entriesArticles)
    # print(rowIndexNavbar)
    #dataPageConfigurationNavbar[0]["configuration"]["templates"][selectedTemplate]["menu"]["articles"]
    newArticleValues = []

    for row in entriesArticles:
        newArticleValues.append({"title": row[0].get(), "text": row[1].get(), "link": row[2].get(), "visile": True})

    db_collection_pageConfiguration.update_one({"_id":"pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(selectedTemplate)}.menu.articles": newArticleValues}})
    print(newArticleValues)

#########################################################################################################

frameNews = {}
selectedBlockNewsName = ""
entriesNews = []
selectedComponentIndex = None


def show_news_or_edit_content_news(page_name, type):
    global sheetNews
    global selectedTemplate
    global dataPageConfigurationNewsComponents
    global selectedBlockNewsName
    global entriesNews
    global selectedComponentIndex

    print("POWINNO SIE WYSTWIELIC")
    print(page_name)
    print(frameNews)

    isSelected = True

    if type == "Edit":
        for widget in NewsEdit.winfo_children():
            widget.destroy()

        NewsEdit.columnconfigure(0, weight=1)
        NewsEdit.columnconfigure(1, weight=1)
        NewsEdit.columnconfigure(2, weight=1)
        NewsEdit.columnconfigure(3, weight=1)

        newsColumnHeaderTitleLabel = ttk.Label(NewsEdit, text="Title")
        newsColumnHeaderTitleLabel.grid(column=0, row=1, padx=5, pady=5)
        newsColumnHeaderTextLabel = ttk.Label(NewsEdit, text="Headline")
        newsColumnHeaderTextLabel.grid(column=1, row=1, padx=5, pady=5)
        newsColumnHeaderTextLabel = ttk.Label(NewsEdit, text="Text")
        newsColumnHeaderTextLabel.grid(column=2, row=1, padx=5, pady=5)
        newsColumnHeaderLinkLabel = ttk.Label(NewsEdit, text="Link")
        newsColumnHeaderLinkLabel.grid(column=3, row=1, padx=5, pady=5)

        rowIndexNavbar = 0

        try:
            selectedRow = next(iter(sheetNews.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))  
            print(sheetNews.get_row_data(selectedRow, return_copy = True)[0])
            selectedBlockNewsName = sheetNews.get_row_data(selectedRow, return_copy = True)[0]

            UsersButtonsFrameEditNews = ttk.Frame(NewsEdit, width=600)
            UsersButtonsFrameEditNews.grid(column=1, columnspan=2, row=0, padx=5, pady=10)
            cancelBtnNews = ttk.Button(UsersButtonsFrameEditNews, text="Cancel", command= lambda: show_news_or_edit_content_news("NewsDefault", "cancel"))
            cancelBtnNews.pack()
            #print(dataPageConfigurationNewsComponents[sheetNews.get_row_data(selectedRow, return_copy = True)[0]])

            print()
            entriesNews = []

            for i,component in enumerate(dataPageConfigurationNewsComponents):
                if component["name"] == sheetNews.get_row_data(selectedRow, return_copy = True)[0]:
                    selectedComponentIndex = i
                    for j,news in enumerate(component['news']):
                        print(news)
                        newsEntryTitle = ttk.Entry(NewsEdit, width=15)
                        newsEntryTitle.grid(column=0, row=j + 2, padx=2, pady=5)
                        newsEntryTitle.insert(0, news["title"])
                        newsEntryHeadline = ttk.Entry(NewsEdit, width=15)
                        newsEntryHeadline.grid(column=1, row=j + 2, padx=2, pady=5)
                        newsEntryHeadline.insert(0, news["headline"])
                        newsEntryText = ttk.Entry(NewsEdit, width=15)
                        newsEntryText.grid(column=2, row=j + 2, padx=2, pady=5)
                        newsEntryText.insert(0, news["text"])
                        newsEntryLink = ttk.Entry(NewsEdit, width=15)
                        newsEntryLink.grid(column=3, row=j + 2, padx=2, pady=5)
                        newsEntryLink.insert(0, news["link"])
                        rowIndexNavbar = j + 2
                        entriesNews.append([newsEntryTitle, newsEntryHeadline, newsEntryText, newsEntryLink])

            rowIndexNavbar += 1

            UsersButtonsFrameEditNewsSave = ttk.Frame(NewsEdit, width=600)
            UsersButtonsFrameEditNewsSave.grid(column=1, columnspan=2, row=rowIndexNavbar, padx=5, pady=15)
            saveBtnNews = ttk.Button(UsersButtonsFrameEditNewsSave, text="Save", command= lambda: show_news_or_edit_content_news("NewsDefault", "Save"))
            saveBtnNews.pack()
        except Exception as exception:
            isSelected = False
            tk.messagebox.showinfo("showinfo", "Block news is not selected, you have to click on the number of row")
    elif type == "Save":
        newNewsValues = []
        for newsEntry in entriesNews:
            newNewsValues.append({"title": newsEntry[0].get(), "headline": newsEntry[1].get(),"text": newsEntry[2].get(),"link": newsEntry[3].get()})

        print(newNewsValues)
        print(selectedComponentIndex)
        db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(selectedTemplate)}.components.{str(selectedComponentIndex)}.news": newNewsValues}})
        load_data_to_news_sheet()
   
    if isSelected:
        for frame in frameNews.keys():
            if frame == page_name:
                frameNews[frame].pack()
            else:
                frameNews[frame].pack_forget()


def load_data_to_news_sheet():
    global sheetNews
    global selectedTemplate
    global dataPageConfigurationNewsComponents

    dataPageConfigurationNews = db_collection_pageConfiguration.find({}, {})
    selectedTemplate = dataPageConfigurationNews[0]["configuration"]["selectedTemplate"]
    dataPageConfigurationNewsComponents = dataPageConfigurationNews[0]["configuration"]["templates"][selectedTemplate]["components"]

    newsBlockNameArray = []

    for component in dataPageConfigurationNewsComponents:
        if len(component["news"]) > 0:
            newsBlockNameArray.append(component["name"])

    sheetNews.set_sheet_data([[newsBlockName] for newsBlockName in newsBlockNameArray])



NewsEdit = ttk.Frame(News, width=600, height=300)
NewsEdit.pack(side="left")
NewsDefault = ttk.Frame(News, width=600, height=300)
NewsDefault.pack(side="left")
frameNews = {"NewsEdit": NewsEdit, "NewsDefault": NewsDefault}


NewsEditButtonFrame = ttk.Frame(NewsDefault, width=300)
NewsEditButtonFrame.pack(side="top")
newsEditButton = ttk.Button(NewsEditButtonFrame, text="Edit", command=lambda: show_news_or_edit_content_news("NewsEdit", "Edit"))
newsEditButton.pack(side="left", pady=10, padx=5)


sheetNews = Sheet(NewsDefault, width=570, enable_edit_cell_auto_resize = False, column_width=390)
sheetNews.pack(side="bottom")

sheetNews.headers(newheaders = ["Block name"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
#RAZ TRZEBA () A RAZ (()), NIE WIEM CZEMU
sheetNews.enable_bindings(("row_select","single_select"))
# load_data_to_sheet()

show_news_or_edit_content_news("NewsDefault", "")


#########################################################################################################

entriesComponentNames = []


def save_components_name_changes():
    global selectedTemplate
    global pageConfiguration
    global entriesComponentNames

    for componentIndex in range(len(pageConfiguration["configuration"]["templates"][selectedTemplate]["components"])): 
        db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(selectedTemplate)}.components.{str(componentIndex)}.name": entriesComponentNames[componentIndex].get()}})

def load_data_to_footer_section():
    global selectedTemplate
    global pageConfiguration
    global entriesComponentNames
    entriesComponentNames = []

    for widget in Footer.winfo_children():
        widget.destroy()

    titleFooterLabel = ttk.Label(Footer, text="Component name")
    titleFooterLabel.pack(padx=10, pady=10)


    pageConfiguration = db_collection_pageConfiguration.find_one({"_id": "pageConfigurationSettings"})
    selectedTemplate = pageConfiguration["configuration"]["selectedTemplate"]
    for component in pageConfiguration["configuration"]["templates"][selectedTemplate]["components"]:
        componentNameEnty = ttk.Entry(Footer)
        componentNameEnty.pack(padx=5, pady=5)
        componentNameEnty.insert(0, component["name"])
        entriesComponentNames.append(componentNameEnty)

    saveComponentNamesChangesBtn = ttk.Button(Footer, text="Save", command=save_components_name_changes)
    saveComponentNamesChangesBtn.pack(padx=10, pady=10)


#########################################################################################################

frameSlider = {}
selectedBlockSliderName = ""
entriesSliderSettings = []
selectedComponentIndexSlider = None


def show_sliders_or_edit_content_slider(page_name, type):
    global sheetSliders
    global selectedTemplate
    global dataPageConfigurationSlidersComponents
    global selectedBlockSliderName
    global entriesSliderSettings
    global selectedComponentIndexSlider

    # print("POWINNO SIE WYSTWIELIC")
    # print(page_name)
    # print(frameNews)

    isSelected = True

    if type == "Edit":
        for widget in SliderEdit.winfo_children():
            widget.destroy()

        SliderEdit.columnconfigure(0, weight=1)
        SliderEdit.columnconfigure(1, weight=1)
        

        sliderColumnHeaderDescriptionLabel = ttk.Label(SliderEdit, text="Description")
        sliderColumnHeaderDescriptionLabel.grid(column=0, row=1, padx=5, pady=5)
        sliderColumnHeaderDurationLabel = ttk.Label(SliderEdit, text="Duration(secs)")
        sliderColumnHeaderDurationLabel.grid(column=1, row=1, padx=5, pady=5)
       

        rowIndexNavbar = 0

        try:
            selectedRow = next(iter(sheetSliders.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))  
            print(sheetSliders.get_row_data(selectedRow, return_copy = True)[0])
            selectedBlockSliderName = sheetSliders.get_row_data(selectedRow, return_copy = True)[0]

            print("CHECKPOINT CHECKPOINT")

            UsersButtonsFrameCancelSlider = ttk.Frame(SliderEdit, width=600)
            UsersButtonsFrameCancelSlider.grid(column=0, columnspan=2, row=0, padx=5, pady=10)
            cancelBtnSlider = ttk.Button(UsersButtonsFrameCancelSlider, text="Cancel", command= lambda: show_sliders_or_edit_content_slider("SliderDefault", "cancel"))
            cancelBtnSlider.pack()
            #print(dataPageConfigurationNewsComponents[sheetNews.get_row_data(selectedRow, return_copy = True)[0]])

            entriesSliderSettings = []

            for i,component in enumerate(dataPageConfigurationSlidersComponents):
                if component["name"] == sheetSliders.get_row_data(selectedRow, return_copy = True)[0]:
                    selectedComponentIndexSlider = i
                    # for j,slider in enumerate(component['slider']):
                    #     print(slider)
                    print("TES")
                    sliderEntryDescription = ttk.Entry(SliderEdit, width=15)
                    sliderEntryDescription.grid(column=0, row=2, padx=2, pady=5)
                    sliderEntryDescription.insert(0, component["slider"]["description"])
                    sliderEntryDuration = ttk.Entry(SliderEdit, width=15)
                    sliderEntryDuration.grid(column=1, row=2, padx=2, pady=5)
                    sliderEntryDuration.insert(0, str(component["slider"]["switchTime"]))
                    entriesSliderSettings.append([sliderEntryDescription, sliderEntryDuration])

            rowIndexNavbar = 3
            print("tu?")
            UsersButtonsFrameEditSlidersSave = ttk.Frame(SliderEdit, width=600)
            UsersButtonsFrameEditSlidersSave.grid(column=0, columnspan=2, row=rowIndexNavbar, padx=5, pady=15)
            saveBtnSlider = ttk.Button(UsersButtonsFrameEditSlidersSave, text="Save", command= lambda: show_sliders_or_edit_content_slider("SliderDefault", "Save"))
            saveBtnSlider.pack()
        except Exception as exception:
            isSelected = False
            tk.messagebox.showinfo("showinfo", "Block slider is not selected, you have to click on the number of row")
    elif type == "Save":
        # newSliderValues = []


        print(selectedComponentIndexSlider)
        #TODO IMPROVE SAVING(NOW IMAGES ARE REMOVING)
        db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(selectedTemplate)}.components.{str(selectedComponentIndexSlider)}.slider.description": entriesSliderSettings[0][0].get()}})
        db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(selectedTemplate)}.components.{str(selectedComponentIndexSlider)}.slider.switchTime": entriesSliderSettings[0][1].get()}})
        load_data_to_slider_sheet()
   
    if isSelected:
        for frame in frameSlider.keys():
            if frame == page_name:
                frameSlider[frame].pack()
            else:
                frameSlider[frame].pack_forget()


def load_data_to_slider_sheet():
    global sheetSliders
    global selectedTemplate
    global dataPageConfigurationSlidersComponents

    dataPageConfigurationSliders = db_collection_pageConfiguration.find({}, {})
    selectedTemplate = dataPageConfigurationSliders[0]["configuration"]["selectedTemplate"]
    dataPageConfigurationSlidersComponents = dataPageConfigurationSliders[0]["configuration"]["templates"][selectedTemplate]["components"]

    slidersBlockNameArray = []

    print(dataPageConfigurationSlidersComponents)

    for component in dataPageConfigurationSlidersComponents:
        print(component["name"])
        if component["slider"] != None:
            slidersBlockNameArray.append(component["name"])

    sheetSliders.set_sheet_data([[sliderBlockName] for sliderBlockName in slidersBlockNameArray])



SliderEdit = ttk.Frame(Slider, width=600, height=300)
SliderEdit.pack(side="left")
SliderDefault = ttk.Frame(Slider, width=600, height=300)
SliderDefault.pack(side="left")
frameSlider = {"SliderEdit": SliderEdit, "SliderDefault": SliderDefault}


SliderEditButtonFrame = ttk.Frame(SliderDefault, width=300)
SliderEditButtonFrame.pack(side="top")
SliderEditButton = ttk.Button(SliderEditButtonFrame, text="Edit", command=lambda: show_sliders_or_edit_content_slider("SliderEdit", "Edit"))
SliderEditButton.pack(side="left", pady=10, padx=5)


sheetSliders = Sheet(SliderDefault, width=570, enable_edit_cell_auto_resize = False, column_width=390)
sheetSliders.pack(side="bottom")

sheetSliders.headers(newheaders = ["Block name"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
#RAZ TRZEBA () A RAZ (()), NIE WIEM CZEMU
sheetSliders.enable_bindings(("row_select","single_select"))
# load_data_to_sheet()

show_sliders_or_edit_content_slider("SliderDefault", "")

window.mainloop()