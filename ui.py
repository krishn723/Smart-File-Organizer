"""
===========================================================
Smart File Organizer
Professional UI
Author : Krishan Kumar
===========================================================
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import threading
from pathlib import Path

from organizer import FileOrganizer
from search import FileSearch
from stats import FolderStatistics
from logger import OrganizerLogger
from categories import get_category

from utils import (
    get_file_size,
    get_modified_date,
    open_file,
    open_folder,
)

# =====================================================
# COLORS
# =====================================================

BG = "#eef2f7"
WHITE = "#ffffff"
SIDEBAR = "#27374D"
PRIMARY = "#1976D2"
SUCCESS = "#4CAF50"

FONT = ("Segoe UI",10)
FONT_BOLD = ("Segoe UI",10,"bold")
TITLE = ("Segoe UI",18,"bold")


class SmartFileOrganizerUI:

    def __init__(self):

        self.logger = OrganizerLogger()

        self.root = tk.Tk()

        self.root.title("Smart File Organizer")

        self.root.geometry("1450x820")

        self.root.configure(bg=BG)

        self.root.minsize(1200,700)

        self.folder = ""

        self.search_engine = None

        self.organizer = None

        self.statistics = None

        self.selected_category = "All"

        self.folder_var = tk.StringVar()

        self.search_var = tk.StringVar()

        self.create_menu()

        self.create_header()

        self.create_body()

        self.create_sidebar()

        self.create_center()

        self.create_right_panel()

        self.create_footer()

    # =====================================================

    def create_menu(self):

        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(
            menubar,
            tearoff=False
        )

        filemenu.add_command(
            label="Open Folder",
            command=self.select_folder
        )

        filemenu.add_separator()

        filemenu.add_command(
            label="Exit",
            command=self.root.destroy
        )

        menubar.add_cascade(
            label="File",
            menu=filemenu
        )

        helpmenu = tk.Menu(
            menubar,
            tearoff=False
        )

        helpmenu.add_command(
            label="About",
            command=self.about
        )

        menubar.add_cascade(
            label="Help",
            menu=helpmenu
        )

        self.root.config(menu=menubar)

    # =====================================================

    def create_header(self):

        self.header = tk.Frame(
            self.root,
            bg=WHITE,
            height=75
        )

        self.header.pack(
            fill="x"
        )

        title = tk.Label(

            self.header,

            text="Smart File Organizer",

            font=TITLE,

            bg=WHITE,

            fg="#222"

        )

        title.pack(
            side="left",
            padx=20
        )

        self.folder_entry = ttk.Entry(

            self.header,

            textvariable=self.folder_var,

            width=65

        )

        self.folder_entry.pack(

            side="left",

            padx=15

        )

        ttk.Button(

            self.header,

            text="Browse",

            command=self.select_folder

        ).pack(

            side="left"

        )

        tk.Label(

            self.header,

            text="Search",

            bg=WHITE,

            font=FONT_BOLD

        ).pack(

            side="left",

            padx=(40,8)

        )

        self.search_entry = ttk.Entry(

            self.header,

            textvariable=self.search_var,

            width=30

        )

        self.search_entry.pack(

            side="left"

        )

        self.search_entry.bind(

            "<KeyRelease>",

            self.search_files

        )

    # =====================================================

    def create_body(self):

        self.body = tk.Frame(

            self.root,

            bg=BG

        )

        self.body.pack(

            fill="both",

            expand=True

        )

    # =====================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(

            self.body,

            bg=SIDEBAR,

            width=220

        )

        self.sidebar.pack(

            side="left",

            fill="y"

        )

        tk.Label(

            self.sidebar,

            text="Categories",

            fg="white",

            bg=SIDEBAR,

            font=("Segoe UI",15,"bold")

        ).pack(

            pady=15

        )

        self.category_box = tk.Listbox(

            self.sidebar,

            font=("Segoe UI",10),

            height=20,

            activestyle="none"

        )

        self.category_box.pack(

            fill="both",

            expand=True,

            padx=12,

            pady=10

        )

        categories = [

            "All",

            "Images",

            "Documents",

            "Videos",

            "Audio",

            "Python Files",

            "Programming",

            "Archives",

            "Executables",

            "Spreadsheets",

            "Presentations",

            "Others"

        ]

        for item in categories:

            self.category_box.insert(
                "end",
                item
            )

        self.category_box.selection_set(0)

        self.category_box.bind(

            "<<ListboxSelect>>",

            self.filter_category

        )

            # =====================================================

    def create_center(self):

        self.center = tk.Frame(
            self.body,
            bg=BG
        )

        self.center.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        # ==========================================
        # Statistics
        # ==========================================

        self.stats_frame = tk.Frame(
            self.center,
            bg=BG
        )

        self.stats_frame.pack(
            fill="x"
        )

        self.total_card = self.create_card(
            self.stats_frame,
            "Total Files",
            "0"
        )

        self.image_card = self.create_card(
            self.stats_frame,
            "Images",
            "0"
        )

        self.document_card = self.create_card(
            self.stats_frame,
            "Documents",
            "0"
        )

        self.video_card = self.create_card(
            self.stats_frame,
            "Videos",
            "0"
        )

        self.audio_card = self.create_card(
            self.stats_frame,
            "Audio",
            "0"
        )

        # ==========================================
        # Treeview
        # ==========================================

        table_frame = tk.Frame(
            self.center,
            bg=WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns=(

            "Name",

            "Category",

            "Extension",

            "Size",

            "Modified"

        )

        self.tree=ttk.Treeview(

            table_frame,

            columns=columns,

            show="headings"

        )

        self.tree.heading(

            "Name",

            text="File Name"

        )

        self.tree.heading(

            "Category",

            text="Category"

        )

        self.tree.heading(

            "Extension",

            text="Extension"

        )

        self.tree.heading(

            "Size",

            text="Size"

        )

        self.tree.heading(

            "Modified",

            text="Modified"

        )

        self.tree.column(

            "Name",

            width=420

        )

        self.tree.column(

            "Category",

            width=150

        )

        self.tree.column(

            "Extension",

            width=90,

            anchor="center"

        )

        self.tree.column(

            "Size",

            width=120,

            anchor="center"

        )

        self.tree.column(

            "Modified",

            width=170,

            anchor="center"

        )

        scrollbar=ttk.Scrollbar(

            table_frame,

            orient="vertical",

            command=self.tree.yview

        )

        self.tree.configure(

            yscrollcommand=scrollbar.set

        )

        self.tree.pack(

            side="left",

            fill="both",

            expand=True

        )

        scrollbar.pack(

            side="right",

            fill="y"

        )

        self.tree.bind(

            "<Double-1>",

            self.open_selected_file

        )

    # =====================================================

    def create_card(self,parent,title,value):

        card=tk.Frame(

            parent,

            bg=WHITE,

            width=170,

            height=70,

            relief="ridge",

            bd=1

        )

        card.pack(

            side="left",

            padx=6,

            pady=5,

            fill="both",

            expand=True

        )

        tk.Label(

            card,

            text=title,

            bg=WHITE,

            font=("Segoe UI",10)

        ).pack(

            pady=(8,2)

        )

        value_label=tk.Label(

            card,

            text=value,

            bg=WHITE,

            fg=PRIMARY,

            font=("Segoe UI",18,"bold")

        )

        value_label.pack()

        return value_label

    # =====================================================

    def create_right_panel(self):

        self.right=tk.Frame(

            self.body,

            width=320,

            bg=WHITE

        )

        self.right.pack(

            side="right",

            fill="y"

        )

        tk.Label(

            self.right,

            text="Activity Log",

            bg=WHITE,

            font=("Segoe UI",15,"bold")

        ).pack(

            pady=10

        )

        self.log_box=tk.Text(

            self.right,

            width=38,

            height=26,

            font=("Consolas",10)

        )

        self.log_box.pack(

            padx=10,

            pady=5,

            fill="both",

            expand=True

        )

        self.progress=ttk.Progressbar(

            self.right,

            orient="horizontal",

            mode="determinate",

            length=250

        )

        self.progress.pack(

            padx=15,

            pady=10,

            fill="x"

        )

        self.organize_btn=ttk.Button(

            self.right,

            text="Organize Files",

            command=self.organize_files

        )

        self.organize_btn.pack(

            fill="x",

            padx=15,

            pady=5

        )

        self.refresh_btn=ttk.Button(

            self.right,

            text="Refresh",

            command=self.refresh_files

        )

        self.refresh_btn.pack(

            fill="x",

            padx=15,

            pady=5

        )

        self.open_btn=ttk.Button(

            self.right,

            text="Open Selected Folder",

            command=self.open_selected_folder

        )

        self.open_btn.pack(

            fill="x",

            padx=15,

            pady=5

        )

        self.clear_btn=ttk.Button(

            self.right,

            text="Clear Log",

            command=self.clear_log

        )

        self.clear_btn.pack(

            fill="x",

            padx=15,

            pady=5

        )

            # =====================================================

    def create_footer(self):

        self.footer = tk.Frame(
            self.root,
            bg=WHITE,
            height=35
        )

        self.footer.pack(
            fill="x",
            side="bottom"
        )

        self.status_label = tk.Label(

            self.footer,

            text="Ready",

            bg=WHITE,

            anchor="w",

            font=("Segoe UI",9)

        )

        self.status_label.pack(

            side="left",

            padx=10

        )

        self.selected_label = tk.Label(

            self.footer,

            text="Selected : 0",

            bg=WHITE,

            font=("Segoe UI",9)

        )

        self.selected_label.pack(

            side="right",

            padx=15

        )

    # =====================================================

    def about(self):

        messagebox.showinfo(

            "About",

            """

Smart File Organizer

Professional File Management Tool

Developed using

Python

Tkinter

Designed By

Krishan Kumar

"""

        )

    # =====================================================

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder == "":

            return

        self.folder = folder

        self.folder_var.set(folder)

        self.search_engine = FileSearch(folder)

        self.organizer = FileOrganizer(folder)

        self.statistics = FolderStatistics(folder)

        self.refresh_files()

    # =====================================================

    def refresh_files(self):

        if self.search_engine is None:

            return

        self.search_engine.refresh()

        self.load_tree()

        self.update_statistics()

        self.status_label.config(

            text="Folder Loaded"

        )

    # =====================================================

    def load_tree(self):

        self.tree.delete(

            *self.tree.get_children()

        )

        files = self.search_engine.get_all_files()

        for file in files:

            self.tree.insert(

                "",

                "end",

                values=(

                    file.name,

                    get_category(file),

                    file.suffix,

                    get_file_size(file),

                    get_modified_date(file)

                )

            )

        self.status_label.config(

            text=f"{len(files)} Files Loaded"

        )

    # =====================================================

    def search_files(self,event=None):

        if self.search_engine is None:

            return

        keyword = self.search_var.get()

        result = self.search_engine.search(keyword)

        self.tree.delete(

            *self.tree.get_children()

        )

        for file in result:

            self.tree.insert(

                "",

                "end",

                values=(

                    file.name,

                    get_category(file),

                    file.suffix,

                    get_file_size(file),

                    get_modified_date(file)

                )

            )

        self.status_label.config(

            text=f"{len(result)} Results"

        )

    # =====================================================

    def filter_category(self,event=None):

        if self.search_engine is None:

            return

        selected = self.category_box.curselection()

        if not selected:

            return

        category = self.category_box.get(

            selected[0]

        )

        self.tree.delete(

            *self.tree.get_children()

        )

        if category == "All":

            files = self.search_engine.get_all_files()

        else:

            files = self.search_engine.search_category(

                category

            )

        for file in files:

            self.tree.insert(

                "",

                "end",

                values=(

                    file.name,

                    category,

                    file.suffix,

                    get_file_size(file),

                    get_modified_date(file)

                )

            )

        self.status_label.config(

            text=f"{category} : {len(files)} Files"

        )

    # =====================================================

    def update_statistics(self):

        if self.statistics is None:

            return

        self.statistics.refresh()

        data = self.statistics.summary()

        categories = data["Categories"]

        self.total_card.config(

            text=data["Total Files"]

        )

        self.image_card.config(

            text=categories.get(

                "Images",

                0

            )

        )

        self.document_card.config(

            text=categories.get(

                "Documents",

                0

            )

        )

        self.video_card.config(

            text=categories.get(

                "Videos",

                0

            )

        )

        self.audio_card.config(

            text=categories.get(

                "Audio",

                0

            )

        )

            # =====================================================

    def organize_files(self):

        if self.organizer is None:

            messagebox.showwarning(

                "Folder",

                "Please select a folder first."

            )

            return

        self.organize_btn.config(

            state="disabled"

        )

        self.progress["value"] = 0

        self.log_box.delete(

            "1.0",

            "end"

        )

        threading.Thread(

            target=self.start_organizing,

            daemon=True

        ).start()

    # =====================================================

    def start_organizing(self):

        self.logger.session_start()

        summary = self.organizer.organize(

            progress_callback=self.update_progress,

            log_callback=self.update_log

        )

        self.logger.session_end()

        self.root.after(

            0,

            self.finish_organization,

            summary

        )

    # =====================================================

    def finish_organization(self,summary):

        self.refresh_files()

        self.progress["value"] = 100

        self.organize_btn.config(

            state="normal"

        )

        messagebox.showinfo(

            "Completed",

            f"""

Organization Completed Successfully

Total Files : {summary['Total Files']}

Moved : {summary['Moved']}

Skipped : {summary['Skipped']}

Errors : {summary['Errors']}

"""

        )

    # =====================================================

    def update_progress(self,value):

        self.root.after(

            0,

            lambda: self.progress.configure(

                value=value

            )

        )

    # =====================================================

    def update_log(self,message):

        self.logger.info(message)

        self.root.after(

            0,

            lambda:self.append_log(message)

        )

    # =====================================================

    def append_log(self,message):

        self.log_box.insert(

            "end",

            message+"\n"

        )

        self.log_box.see(

            "end"

        )

    # =====================================================

    def clear_log(self):

        self.log_box.delete(

            "1.0",

            "end"

        )

    # =====================================================

    def refresh_selected(self,event=None):

        item=self.tree.focus()

        if not item:

            self.selected_label.config(

                text="Selected : 0"

            )

            return

        self.selected_label.config(

            text="Selected : 1"

        )

    # =====================================================

    def get_selected_path(self):

        item=self.tree.focus()

        if not item:

            return None

        values=self.tree.item(

            item,

            "values"

        )

        filename=values[0]

        for file in Path(self.folder).rglob("*"):

            if file.is_file():

                if file.name==filename:

                    return file

        return None

    # =====================================================

    def open_selected_file(self,event=None):

        file=self.get_selected_path()

        if file:

            open_file(file)

    # =====================================================

    def open_selected_folder(self):

        file=self.get_selected_path()

        if file:

            open_folder(file.parent)

    # =====================================================

    def delete_tree(self):

        self.tree.delete(

            *self.tree.get_children()

        )

    # =====================================================

    def sort_tree(self,column):

        rows=[]

        for child in self.tree.get_children():

            rows.append(

                (

                    self.tree.set(

                        child,

                        column

                    ),

                    child

                )

            )

        rows.sort()

        for index,(_,child) in enumerate(rows):

            self.tree.move(

                child,

                "",

                index

            )

    # =====================================================

    def enable_sorting(self):

        self.tree.heading(

            "Name",

            command=lambda:self.sort_tree("Name")

        )

        self.tree.heading(

            "Category",

            command=lambda:self.sort_tree("Category")

        )

        self.tree.heading(

            "Extension",

            command=lambda:self.sort_tree("Extension")

        )

        self.tree.heading(

            "Size",

            command=lambda:self.sort_tree("Size")

        )

        self.tree.heading(

            "Modified",

            command=lambda:self.sort_tree("Modified")

        )

    # =====================================================

    def run(self):

        self.enable_sorting()

        self.tree.bind(

            "<<TreeviewSelect>>",

            self.refresh_selected

        )

        self.root.mainloop()

# =====================================================
# END OF CLASS
# =====================================================

if __name__=="__main__":

    app=SmartFileOrganizerUI()

    app.run()

    