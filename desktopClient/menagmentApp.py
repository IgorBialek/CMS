from asyncio import events
import enum
from msilib.schema import Component
from operator import index
import tkinter as tk
from tkinter import ttk
import tkinter
from turtle import bgcolor, right, title
from ttkthemes import ThemedTk
from tksheet import Sheet
import pymongo
import re
import ctypes
import os

myappid = 'appIcon.ico' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class App:

    def __init__(self, master):
        # super().__init__(master)
        #self.pack()
        self.master = master

        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.myclient["cms"]
        self.db_collection_users = self.db["users"]
        self.db_collection_pageConfiguration = self.db["pageConfiguration"]

        master.configure(bg='#3dade9')


        try:
            self.db_collection_users.insert_one({ "_id": "admin", "password": "admin", "permission": "admin"})
        except Exception as exception:
            print("Admin already exists")

        self.notebookSections = ttk.Notebook(master)
        #self.notebookSections.pack(anchor='center', expand=True, pady=10)


        self.Users = ttk.Frame(self.notebookSections, width=600, height=300)
        self.init_users_tab()
        self.Navbar = ttk.Frame(self.notebookSections, width=600, height=300)
        self.News = ttk.Frame(self.notebookSections, width=600, height=300)
        self.init_news_tab()
        self.Footer = ttk.Frame(self.notebookSections, width=600, height=300)
        self.Slider = ttk.Frame(self.notebookSections, width=600, height=300)
        self.init_slider_tab()

        self.notebookSections.add(self.Users, text="Users")
        self.notebookSections.add(self.Navbar, text="Navbar")
        self.notebookSections.add(self.News, text="News")
        self.notebookSections.add(self.Footer, text="Footer")
        self.notebookSections.add(self.Slider, text="Slider")
        self.notebookSections.bind('<<NotebookTabChanged>>', self.on_tab_change)

        self.show_login_dialog()


    def show_login_dialog(self):
        self.mainloginFrame = ttk.Frame(self.master,  height=100, width=100)
        self.mainloginFrame.pack(anchor='center', expand=True)

        loginFrameContent = ttk.Frame(self.mainloginFrame,  height=400, width=800)
        loginFrameContent.pack(padx=60, pady=50)
        
        loginFrameLabelLogin = ttk.Label(loginFrameContent, text="Login")
        loginFrameLabelLogin.pack()
        self.loginFrameEntryLogin = ttk.Entry(loginFrameContent, width=25)
        self.loginFrameEntryLogin.pack()

        loginFrameLabelPassword = ttk.Label(loginFrameContent, text="Password")
        loginFrameLabelPassword.pack()
        self.loginFrameEntryPassword = ttk.Entry(loginFrameContent, width=25)
        self.loginFrameEntryPassword.pack()

        loginFrameButtonLogin = ttk.Button(loginFrameContent, text="Login", command= self.validate_login_dialog)
        loginFrameButtonLogin.pack(pady=10, padx=5)

        self.loginFrameLabelInfo = ttk.Label(loginFrameContent, text="")
        self.loginFrameLabelInfo.pack()


    def validate_login_dialog(self):
        if self.loginFrameEntryLogin.get() == "admin" and self.loginFrameEntryPassword.get() == "admin":
            self.mainloginFrame.pack_forget()
            self.notebookSections.pack(anchor='center', expand=True, pady=10)
        else:
            self.loginFrameLabelInfo.config(text="Login or password is not correct")

    
    def init_users_tab(self):

        self.UsersEdit = ttk.Frame(self.Users, width=600, height=300)
        self.UsersEdit.pack(side="left")
        self.UsersDefault = ttk.Frame(self.Users, width=600, height=300)
        self.UsersDefault.pack(side="left", padx=5)
        self.frames = {"UsersDefault": self.UsersDefault, "UsersEdit": self.UsersEdit}
        
        #ELEMENTS
        self.UsersButtonsFrame = ttk.Frame(self.UsersDefault, width=600)
        self.UsersButtonsFrame.pack()

        self.addBtn = ttk.Button(self.UsersButtonsFrame, text="Add", command= lambda: self.show_users_or_edit_content("UsersEdit", "add"))
        self.addBtn.pack(side="left", pady=10, padx=5)

        self.editBtn = ttk.Button(self.UsersButtonsFrame, text="Edit" , command= lambda: self.show_users_or_edit_content("UsersEdit", "edit"))
        self.editBtn.pack(side="left", pady=10, padx=5)

        self.deleteBtn = ttk.Button(self.UsersButtonsFrame, text="Delete", command= lambda: self.delete_user())
        self.deleteBtn.pack(side="left", pady=10, padx=5)

        self.sheet = Sheet(self.UsersDefault, width=570, enable_edit_cell_auto_resize = False)
        self.sheet.pack()
        self.sheet.headers(newheaders = ["email", "password", "permission"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
        self.sheet.enable_bindings("row_select","single_select")

        self.sheet.extra_bindings("all", self.select_whole_row)

        self.load_data_to_sheet()

        #USER EDIT
        self.UsersButtonsFrameEdit = ttk.Frame(self.UsersEdit, width=600)
        self.UsersButtonsFrameEdit.pack()
        self.cancelBtn = ttk.Button(self.UsersButtonsFrameEdit, text="Cancel", command= lambda: self.show_users_or_edit_content("UsersDefault", "cancel"))
        self.cancelBtn.pack(side="left", pady=10, padx=5)

        self.InfoUserEditFrame = ttk.Frame(self.UsersEdit, width=600)
        self.InfoUserEditFrame.pack(side="bottom")
        self.infoLabel = ttk.Label(self.InfoUserEditFrame, text="")
        self.infoLabel.pack()

        self.typeOfSaving = ""
        self.editedUserId = ""
        self.SaveButtonFrame = ttk.Frame(self.UsersEdit, width=600)
        self.SaveButtonFrame.pack(side="bottom")
        self.saveBtn = ttk.Button(self.SaveButtonFrame, text="Save", command= lambda: self.show_users_or_edit_content("UsersDefault", "save"))
        self.saveBtn.pack(side="left", pady=10, padx=5)


        self.PermissionFrame = ttk.Frame(self.UsersEdit, width=300)
        self.PermissionFrame.pack(side="bottom")
        self.permissionLabel = ttk.Label(self.PermissionFrame, text="Permission", width=15)
        self.permissionLabel.pack(side="left")
        self.selected_role = tk.StringVar()
        self.permissionCombobox = ttk.Combobox(self.PermissionFrame, textvariable=self.selected_role, width=24, state = "readonly")
        self.permissionCombobox['values'] = ["admin", "permitted", "user"]
        self.permissionCombobox.pack(side="right")


        self.PasswordRepeatFrame = ttk.Frame(self.UsersEdit, width=300)
        self.PasswordRepeatFrame.pack(side="bottom")
        self.passwordRepeatLabel = ttk.Label(self.PasswordRepeatFrame, text="Password repeat", width=15)
        self.passwordRepeatLabel.pack(side="left")
        self.passwordRepeatEntry = ttk.Entry(self.PasswordRepeatFrame, width=25)
        self.passwordRepeatEntry.pack(side="right")
        self.passwordRepeatEntry.config(validate="focusout", validatecommand=self.check_passwords)
        #passwordRepeatEntry.insert(0, choosedUserPassword)

        self.PasswordFrame = ttk.Frame(self.UsersEdit, width=300)
        self.PasswordFrame.pack(side="bottom")
        self.passwordLabel = ttk.Label(self.PasswordFrame, text="Password", width=15)
        self.passwordLabel.pack(side="left")
        self.passwordEntry = ttk.Entry(self.PasswordFrame, width=25)
        self.passwordEntry.pack(side="right")

        self.UsersEmailFrame = ttk.Frame(self.UsersEdit, width=300)
        self.UsersEmailFrame.pack(side="bottom")
        self.emailLabel = ttk.Label(self.UsersEmailFrame, text="Email", width=15)
        self.emailLabel.pack(side="left")
        self.emailEntry = ttk.Entry(self.UsersEmailFrame, width=25 )
        self.emailEntry.config(validate="focusout", validatecommand=self.check_email)
        self.emailEntry.pack(side="right")

        self.show_users_or_edit_content("UsersDefault", "")


    def init_news_tab(self):
        self.selectedBlockNewsName = ""
        self.entriesNews = []
        self.selectedComponentIndex = None

        self.NewsEdit = ttk.Frame(self.News, width=600, height=300)
        self.NewsEdit.pack(side="left")
        self.NewsDefault = ttk.Frame(self.News, width=600, height=300)
        self.NewsDefault.pack(side="left")
        self.frameNews = {"NewsEdit": self.NewsEdit, "NewsDefault": self.NewsDefault}

        self.NewsEditButtonFrame = ttk.Frame(self.NewsDefault, width=300)
        self.NewsEditButtonFrame.pack(side="top")
        self.newsEditButton = ttk.Button(self.NewsEditButtonFrame, text="Edit", command=lambda: self.show_news_or_edit_content_news("NewsEdit", "Edit"))
        self.newsEditButton.pack(side="left", pady=10, padx=5)

        self.sheetNews = Sheet(self.NewsDefault, width=570, enable_edit_cell_auto_resize = False, column_width=390)
        self.sheetNews.pack(side="bottom")
        self.sheetNews.headers(newheaders = ["Block name"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
        self.sheetNews.enable_bindings("row_select","single_select")
        self.sheetNews.extra_bindings("all", self.select_whole_row_news)


        self.show_news_or_edit_content_news("NewsDefault", "")



    def init_slider_tab(self):
        self.selectedBlockSliderName = ""
        self.entriesSliderSettings = []
        self.selectedComponentIndexSlider = None

        self.SliderEdit = ttk.Frame(self.Slider, width=600, height=300)
        self.SliderEdit.pack(side="left")
        self.SliderDefault = ttk.Frame(self.Slider, width=600, height=300)
        self.SliderDefault.pack(side="left")
        self.frameSlider = {"SliderEdit": self.SliderEdit, "SliderDefault": self.SliderDefault}


        self.SliderEditButtonFrame = ttk.Frame(self.SliderDefault, width=300)
        self.SliderEditButtonFrame.pack(side="top")
        self.SliderEditButton = ttk.Button(self.SliderEditButtonFrame, text="Edit", command=lambda: self.show_sliders_or_edit_content_slider("SliderEdit", "Edit"))
        self.SliderEditButton.pack(side="left", pady=10, padx=5)


        self.sheetSliders = Sheet(self.SliderDefault, width=570, enable_edit_cell_auto_resize = False, column_width=390)
        self.sheetSliders.pack(side="bottom")

        self.sheetSliders.headers(newheaders = ["Block name"], index = None, reset_col_positions = False, show_headers_if_not_sheet = True)
        self.sheetSliders.enable_bindings("row_select","single_select")
        self.sheetSliders.extra_bindings("all", self.select_whole_row_sliders)


        self.show_sliders_or_edit_content_slider("SliderDefault", "")


    def on_tab_change(self, event):
        tab = event.widget.tab('current')['text']
        print(tab)

        if tab == "Users":
            self.load_data_to_sheet()
        elif tab == "Navbar":
            self.load_data_to_navbar_section()
        elif tab == "News":
            self.load_data_to_news_sheet()
        elif tab == "Footer":
            self.load_data_to_footer_section()
        elif tab == "Slider":
            self.load_data_to_slider_sheet()


    ########################USERS

    def select_whole_row(self, event = None):
        if event[0] == "select_cell":
            print(self.sheet.get_currently_selected(get_coords = False, return_nones_if_not = False)[0])
            self.sheet.select_row(self.sheet.get_currently_selected(get_coords = False, return_nones_if_not = False)[0], redraw = False)

    def select_whole_row_news(self, event = None):
        if event[0] == "select_cell":
            print(self.sheetNews.get_currently_selected(get_coords = False, return_nones_if_not = False)[0])
            self.sheetNews.select_row(self.sheetNews.get_currently_selected(get_coords = False, return_nones_if_not = False)[0], redraw = False)


    def select_whole_row_sliders(self, event = None):
            if event[0] == "select_cell":
                print(self.sheetSliders.get_currently_selected(get_coords = False, return_nones_if_not = False)[0])
                self.sheetSliders.select_row(self.sheetSliders.get_currently_selected(get_coords = False, return_nones_if_not = False)[0], redraw = False)

    def load_data_to_sheet(self):

        try:
            self.sheet.set_sheet_data([[user["_id"], user["password"], user["permission"]] for user in self.db_collection_users.find({}, {})])
        except:
            print("Page is laoding")


    def insert_user(self, email, password, permission):

        if self.typeOfSaving == "edit":
            self.db_collection_users.delete_one({ "_id": self.editedUserId})

        self.db_collection_users.insert_one({ "_id": email, "password": password, "permission": permission })
        self.load_data_to_sheet()


    def delete_user(self):
        try:
            sheetData = next(iter(self.sheet.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))  
            if self.sheet.get_row_data(sheetData, return_copy = True)[0] == "admin":
                raise ValueError('A very specific bad thing happened.')

            self.db_collection_users.delete_one({"_id": self.sheet.get_row_data(sheetData, return_copy = True)[0], "password": self.sheet.get_row_data(sheetData, return_copy = True)[1], "permission": self.sheet.get_row_data(sheetData, return_copy = True)[2]})
            self.sheet.deselect(row = sheetData, column = None, cell = None, redraw = True)
            self.load_data_to_sheet()
        except ValueError as valueException:
                tk.messagebox.showinfo("showinfo", "You cannot delete main admin!")
                return
        except Exception as exception:
            tk.messagebox.showinfo("showinfo", "User is not selected, you have to click on the number of row")
            

    def show_users_or_edit_content(self, page_name, type):

        emailIsValid = True
        passwordIsValid = True

        if page_name == "UsersEdit":
            self.emailEntry.delete(0, 'end')
            self.passwordEntry.delete(0, 'end')
            self.passwordRepeatEntry.delete(0, 'end')       

        if type == "edit":
            try:
                sheetData = next(iter(self.sheet.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))                
                if self.sheet.get_row_data(sheetData, return_copy = True)[0] == "admin":
                    raise ValueError('A very specific bad thing happened.')

                self.emailEntry.insert(0, self.sheet.get_row_data(sheetData, return_copy = True)[0])
                self.passwordEntry.insert(0, self.sheet.get_row_data(sheetData, return_copy = True)[1])
                self.passwordRepeatEntry.insert(0, self.sheet.get_row_data(sheetData, return_copy = True)[1])
                self.permissionCombobox.set( self.sheet.get_row_data(sheetData, return_copy = True)[2])
                self.typeOfSaving = "edit"
                self.editedUserId = self.sheet.get_row_data(sheetData, return_copy = True)[0]
            except ValueError as valueException:
                tk.messagebox.showinfo("showinfo", "You cannot edit main admin!")
                return
            except Exception as exception:
                tk.messagebox.showinfo("showinfo", "User is not selected, you have to click on the number of row")
                return
        elif type == "add":
                self.typeOfSaving = "add"
                self.permissionCombobox.set("user")
        elif type == "save":
            emailIsValid = self.emailEntry.validate()
            passwordIsValid = self.passwordRepeatEntry.validate()

            if emailIsValid and passwordIsValid:
                self.insert_user(self.emailEntry.get(), self.passwordEntry.get(), self.permissionCombobox.get())


        print(page_name)
        print(self.frames)


        if emailIsValid and passwordIsValid:
            for frame in self.frames.keys():
                if frame == page_name:
                    self.frames[frame].pack()
                else:
                    self.frames[frame].pack_forget()


    def check_email(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        
        if re.search(regex, self.emailEntry.get()):
            self.infoLabel.config(text="")
            return True
        else:
            self.infoLabel.config(text="Email is not valid")
            return False


    def check_passwords(self):

        if len(self.passwordEntry.get()) > 0 and len(self.passwordRepeatEntry.get()) > 0 and self.passwordRepeatEntry.get() == self.passwordEntry.get():
            self.infoLabel.config(text="")
            return True
        else:
            self.infoLabel.config(text="Passwords must be equal and cannot be empty")
            return False

    ##################################NAVBAR

    def load_data_to_navbar_section(self):

        self.entriesArticles = []

        for widget in self.Navbar.winfo_children():
            widget.destroy()

        self.Navbar.columnconfigure(0, weight=1)
        self.Navbar.columnconfigure(1, weight=1)
        self.Navbar.columnconfigure(2, weight=1)

        navbarColumnHeaderTitleLabel = ttk.Label(self.Navbar, text="Title")
        navbarColumnHeaderTitleLabel.grid(column=0, row=0, padx=5, pady=5)
        navbarColumnHeaderTextLabel = ttk.Label(self.Navbar, text="Text")
        navbarColumnHeaderTextLabel.grid(column=1, row=0, padx=5, pady=5)
        navbarColumnHeaderLinkLabel = ttk.Label(self.Navbar, text="Link")
        navbarColumnHeaderLinkLabel.grid(column=2, row=0, padx=5, pady=5)

        #print(type(db_collection_pageConfiguration.find({}, {})))

        dataPageConfigurationNavbar = self.db_collection_pageConfiguration.find({}, {})
        self.selectedTemplate = dataPageConfigurationNavbar[0]["configuration"]["selectedTemplate"]
        self.dataPageConfigurationNavbarArticles = dataPageConfigurationNavbar[0]["configuration"]["templates"][self.selectedTemplate]["menu"]["articles"]


        rowIndexNavbar = 0

        for i,article in enumerate(self.dataPageConfigurationNavbarArticles):
            print(article['title'])
            self.articleEntryTitle = ttk.Entry(self.Navbar)
            self.articleEntryTitle.grid(column=0, row=i + 1, padx=5, pady=5)
            self.articleEntryTitle.insert(0, article["title"])
            self.articleEntryText = ttk.Entry(self.Navbar)
            self.articleEntryText.grid(column=1, row=i + 1, padx=5, pady=5)
            self.articleEntryText.insert(0, article["text"])
            self.articleEntryLink = ttk.Entry(self.Navbar)
            self.articleEntryLink.grid(column=2, row=i + 1, padx=5, pady=5)
            self.articleEntryLink.insert(0, article["link"])
            rowIndexNavbar = i + 1
            self.entriesArticles.append([self.articleEntryTitle, self.articleEntryText, self.articleEntryLink])

        rowIndexNavbar += 1

        saveArticlesNavbar = ttk.Button(self.Navbar, text="Save", command=self.save_articles)
        saveArticlesNavbar.grid(column=1, row=rowIndexNavbar, padx=5, pady=5)


    def save_articles(self):   
        self.newArticleValues = []
        for row in self.entriesArticles:
            self.newArticleValues.append({"title": row[0].get(), "text": row[1].get(), "link": row[2].get(), "visible": True})

        self.db_collection_pageConfiguration.update_one({"_id":"pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(self.selectedTemplate)}.menu.articles": self.newArticleValues}})


    ################################NEWS


    def show_news_or_edit_content_news(self, page_name, type):

        isSelected = True

        if type == "Edit":
            for widget in self.NewsEdit.winfo_children():
                widget.destroy()

            self.NewsEdit.columnconfigure(0, weight=1)
            self.NewsEdit.columnconfigure(1, weight=1)
            self.NewsEdit.columnconfigure(2, weight=1)
            self.NewsEdit.columnconfigure(3, weight=1)

            self.newsColumnHeaderTitleLabel = ttk.Label(self.NewsEdit, text="Title")
            self.newsColumnHeaderTitleLabel.grid(column=0, row=1, padx=5, pady=5)
            self.newsColumnHeaderTextLabel = ttk.Label(self.NewsEdit, text="Headline")
            self.newsColumnHeaderTextLabel.grid(column=1, row=1, padx=5, pady=5)
            self.newsColumnHeaderTextLabel = ttk.Label(self.NewsEdit, text="Text")
            self.newsColumnHeaderTextLabel.grid(column=2, row=1, padx=5, pady=5)
            self.newsColumnHeaderLinkLabel = ttk.Label(self.NewsEdit, text="Link")
            self.newsColumnHeaderLinkLabel.grid(column=3, row=1, padx=5, pady=5)

            rowIndexNavbar = 0

            try:
                self.selectedRow = next(iter(self.sheetNews.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))  
                self.selectedBlockNewsName = self.sheetNews.get_row_data(self.selectedRow, return_copy = True)[0]

                self.UsersButtonsFrameEditNews = ttk.Frame(self.NewsEdit, width=600)
                self.UsersButtonsFrameEditNews.grid(column=1, columnspan=2, row=0, padx=5, pady=10)
                self.cancelBtnNews = ttk.Button(self.UsersButtonsFrameEditNews, text="Cancel", command= lambda: self.show_news_or_edit_content_news("NewsDefault", "cancel"))
                self.cancelBtnNews.pack()

                self.entriesNews = []

                for i,component in enumerate(self.dataPageConfigurationNewsComponents):
                    if component["name"] == self.sheetNews.get_row_data(self.selectedRow, return_copy = True)[0]:
                        self.selectedComponentIndex = i
                        for j,news in enumerate(component['news']):
                            print(news)
                            self.newsEntryTitle = ttk.Entry(self.NewsEdit, width=15)
                            self.newsEntryTitle.grid(column=0, row=j + 2, padx=2, pady=5)
                            self.newsEntryTitle.insert(0, news["title"])
                            self.newsEntryHeadline = ttk.Entry(self.NewsEdit, width=15)
                            self.newsEntryHeadline.grid(column=1, row=j + 2, padx=2, pady=5)
                            self.newsEntryHeadline.insert(0, news["headline"])
                            self.newsEntryText = ttk.Entry(self.NewsEdit, width=15)
                            self.newsEntryText.grid(column=2, row=j + 2, padx=2, pady=5)
                            self.newsEntryText.insert(0, news["text"])
                            self.newsEntryLink = ttk.Entry(self.NewsEdit, width=15)
                            self.newsEntryLink.grid(column=3, row=j + 2, padx=2, pady=5)
                            self.newsEntryLink.insert(0, news["link"])
                            rowIndexNavbar = j + 2
                            self.entriesNews.append([self.newsEntryTitle, self.newsEntryHeadline, self.newsEntryText, self.newsEntryLink])

                rowIndexNavbar += 1

                self.UsersButtonsFrameEditNewsSave = ttk.Frame(self.NewsEdit, width=600)
                self.UsersButtonsFrameEditNewsSave.grid(column=1, columnspan=2, row=rowIndexNavbar, padx=5, pady=15)
                self.saveBtnNews = ttk.Button(self.UsersButtonsFrameEditNewsSave, text="Save", command= lambda: self.show_news_or_edit_content_news("NewsDefault", "Save"))
                self.saveBtnNews.pack()
            except Exception as exception:
                isSelected = False
                tk.messagebox.showinfo("showinfo", "Block news is not selected, you have to click on the number of row")
        elif type == "Save":
            self.newNewsValues = []
            for newsEntry in self.entriesNews:
                self.newNewsValues.append({"title": newsEntry[0].get(), "headline": newsEntry[1].get(),"text": newsEntry[2].get(),"link": newsEntry[3].get()})

            self.db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(self.selectedTemplate)}.components.{str(self.selectedComponentIndex)}.news": self.newNewsValues}})
            self.load_data_to_news_sheet()
    
        if isSelected:
            for frame in self.frameNews.keys():
                if frame == page_name:
                    self.frameNews[frame].pack()
                else:
                    self.frameNews[frame].pack_forget()


    def load_data_to_news_sheet(self):

        self.dataPageConfigurationNews = self.db_collection_pageConfiguration.find({}, {})
        self.selectedTemplate = self.dataPageConfigurationNews[0]["configuration"]["selectedTemplate"]
        self.dataPageConfigurationNewsComponents = self.dataPageConfigurationNews[0]["configuration"]["templates"][self.selectedTemplate]["components"]

        self.newsBlockNameArray = []

        for component in self.dataPageConfigurationNewsComponents:
            if len(component["news"]) > 0:
                self.newsBlockNameArray.append(component["name"])

        self.sheetNews.set_sheet_data([[newsBlockName] for newsBlockName in self.newsBlockNameArray])


    #########################FOOTER


    def save_components_name_changes(self):
        for componentIndex in range(len(self.pageConfiguration["configuration"]["templates"][self.selectedTemplate]["components"])): 
            self.db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(self.selectedTemplate)}.components.{str(componentIndex)}.name": self.entriesComponentNames[componentIndex].get()}})

    def load_data_to_footer_section(self):
        self.entriesComponentNames = []

        for widget in self.Footer.winfo_children():
            widget.destroy()

        self.titleFooterLabel = ttk.Label(self.Footer, text="Component name")
        self.titleFooterLabel.pack(padx=10, pady=10)


        self.pageConfiguration = self.db_collection_pageConfiguration.find_one({"_id": "pageConfigurationSettings"})
        self.selectedTemplate = self.pageConfiguration["configuration"]["selectedTemplate"]
        for component in self.pageConfiguration["configuration"]["templates"][self.selectedTemplate]["components"]:
            self.componentNameEnty = ttk.Entry(self.Footer)
            self.componentNameEnty.pack(padx=5, pady=5)
            self.componentNameEnty.insert(0, component["name"])
            self.entriesComponentNames.append(self.componentNameEnty)

        self.saveComponentNamesChangesBtn = ttk.Button(self.Footer, text="Save", command=self.save_components_name_changes)
        self.saveComponentNamesChangesBtn.pack(padx=10, pady=10)

    ############################SLIDER
    def show_sliders_or_edit_content_slider(self, page_name, type):
        isSelected = True
        durationIsValid = True

        if type == "Edit":
            for widget in self.SliderEdit.winfo_children():
                widget.destroy()

            self.SliderEdit.columnconfigure(0, weight=1)
            self.SliderEdit.columnconfigure(1, weight=1)
            

            self.sliderColumnHeaderDescriptionLabel = ttk.Label(self.SliderEdit, text="Description")
            self.sliderColumnHeaderDescriptionLabel.grid(column=0, row=1, padx=5, pady=5)
            self.sliderColumnHeaderDurationLabel = ttk.Label(self.SliderEdit, text="Duration(secs)")
            self.sliderColumnHeaderDurationLabel.grid(column=1, row=1, padx=5, pady=5)
        

            rowIndexNavbar = 0

            try:
                self.selectedRow = next(iter(self.sheetSliders.get_selected_rows(get_cells = False, get_cells_as_rows = False, return_tuple = False)))  
                self.selectedBlockSliderName = self.sheetSliders.get_row_data(self.selectedRow, return_copy = True)[0]

                self.UsersButtonsFrameCancelSlider = ttk.Frame(self.SliderEdit, width=600)
                self.UsersButtonsFrameCancelSlider.grid(column=0, columnspan=2, row=0, padx=5, pady=10)
                self.cancelBtnSlider = ttk.Button(self.UsersButtonsFrameCancelSlider, text="Cancel", command= lambda: self.show_sliders_or_edit_content_slider("SliderDefault", "cancel"))
                self.cancelBtnSlider.pack()
                self.entriesSliderSettings = []

                for i,component in enumerate(self.dataPageConfigurationSlidersComponents):
                    if component["name"] == self.sheetSliders.get_row_data(self.selectedRow, return_copy = True)[0]:
                        self.selectedComponentIndexSlider = i
                        self.sliderEntryDescription = ttk.Entry(self.SliderEdit, width=15)
                        self.sliderEntryDescription.grid(column=0, row=2, padx=2, pady=5)
                        self.sliderEntryDescription.insert(0, component["slider"]["description"])
                        self.sliderEntryDuration = ttk.Entry(self.SliderEdit, width=15)
                        self.sliderEntryDuration.grid(column=1, row=2, padx=2, pady=5)
                        self.sliderEntryDuration.insert(0, str(component["slider"]["switchTime"]))
                        self.sliderEntryDuration.config(validate="focusout", validatecommand=self.slider_duration_validate)
                        self.entriesSliderSettings.append([self.sliderEntryDescription, self.sliderEntryDuration])

                rowIndexNavbar = 3
                self.UsersButtonsFrameEditSlidersSave = ttk.Frame(self.SliderEdit, width=600)
                self.UsersButtonsFrameEditSlidersSave.grid(column=0, columnspan=2, row=rowIndexNavbar, padx=5, pady=15)
                self.saveBtnSlider = ttk.Button(self.UsersButtonsFrameEditSlidersSave, text="Save", command= lambda: self.show_sliders_or_edit_content_slider("SliderDefault", "Save"))
                self.saveBtnSlider.pack()
                self.sliderLabelInfo = ttk.Label(self.UsersButtonsFrameEditSlidersSave, width=35)
                self.sliderLabelInfo.pack()

            except Exception as exception:
                isSelected = False
                tk.messagebox.showinfo("showinfo", "Block slider is not selected, you have to click on the number of row")
        elif type == "Save":
            durationIsValid = self.sliderEntryDuration.validate()

            if durationIsValid:
                self.db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(self.selectedTemplate)}.components.{str(self.selectedComponentIndexSlider)}.slider.description": self.entriesSliderSettings[0][0].get()}})
                self.db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"$set": {f"configuration.templates.{str(self.selectedTemplate)}.components.{str(self.selectedComponentIndexSlider)}.slider.switchTime": self.entriesSliderSettings[0][1].get()}})
                self.load_data_to_slider_sheet()
    
        if isSelected and durationIsValid:
            for frame in self.frameSlider.keys():
                if frame == page_name:
                    self.frameSlider[frame].pack()
                else:
                    self.frameSlider[frame].pack_forget()


    def slider_duration_validate(self):
        print(self.sliderEntryDuration.get())
        if self.sliderEntryDuration.get() != "":
            try:
                float(self.sliderEntryDuration.get())
                return True
            except ValueError:
                self.sliderLabelInfo.config(text="Duration field has to be empty or a number")
                return False
        else:
            return True

    def load_data_to_slider_sheet(self):

        self.dataPageConfigurationSliders = self.db_collection_pageConfiguration.find({}, {})
        self.selectedTemplate = self.dataPageConfigurationSliders[0]["configuration"]["selectedTemplate"]
        self.dataPageConfigurationSlidersComponents = self.dataPageConfigurationSliders[0]["configuration"]["templates"][self.selectedTemplate]["components"]

        self.slidersBlockNameArray = []


        for component in self.dataPageConfigurationSlidersComponents:
            print(component["name"])
            if component["slider"] != None:
                self.slidersBlockNameArray.append(component["name"])

        self.sheetSliders.set_sheet_data([[sliderBlockName] for sliderBlockName in self.slidersBlockNameArray])


window = ThemedTk(theme="breeze")
window.geometry("900x500")
window.title("Menagment")
# window.configure(bg='#3dade9')

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
window.iconbitmap(os.path.join(__location__, 'appIcon.ico'))

app = App(window)

window.mainloop()

