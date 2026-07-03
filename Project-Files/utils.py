"""
utils.py
=========================================
Smart File Organizer
Final Version
=========================================
"""

import os
import platform
import subprocess
from pathlib import Path
from datetime import datetime


# ======================================================
# HUMAN READABLE SIZE
# ======================================================

def format_size(size):

    units = [

        "B",

        "KB",

        "MB",

        "GB",

        "TB"

    ]

    size = float(size)

    for unit in units:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


# ======================================================
# FILE SIZE
# ======================================================

def get_file_size(file_path):

    try:

        return format_size(

            os.path.getsize(file_path)

        )

    except:

        return "Unknown"


# ======================================================
# FILE NAME
# ======================================================

def get_filename(file_path):

    return Path(file_path).name


# ======================================================
# FILE EXTENSION
# ======================================================

def get_extension(file_path):

    return Path(file_path).suffix.lower()


# ======================================================
# FILE STEM
# ======================================================

def get_stem(file_path):

    return Path(file_path).stem


# ======================================================
# CREATED DATE
# ======================================================

def get_created_date(file_path):

    try:

        timestamp = os.path.getctime(file_path)

        return datetime.fromtimestamp(

            timestamp

        ).strftime(

            "%d-%m-%Y %H:%M"

        )

    except:

        return "Unknown"


# ======================================================
# MODIFIED DATE
# ======================================================

def get_modified_date(file_path):

    try:

        timestamp = os.path.getmtime(file_path)

        return datetime.fromtimestamp(

            timestamp

        ).strftime(

            "%d-%m-%Y %H:%M"

        )

    except:

        return "Unknown"


# ======================================================
# UNIQUE FILE NAME
# ======================================================

def get_unique_filename(

    destination_folder,

    filename

):

    destination_folder = Path(

        destination_folder

    )

    file = destination_folder / filename

    if not file.exists():

        return file

    stem = file.stem

    suffix = file.suffix

    counter = 1

    while True:

        new_file = destination_folder / (

            f"{stem} ({counter}){suffix}"

        )

        if not new_file.exists():

            return new_file

        counter += 1


# ======================================================
# OPEN FILE
# ======================================================

def open_file(file_path):

    try:

        system = platform.system()

        if system == "Windows":

            os.startfile(file_path)

        elif system == "Darwin":

            subprocess.call(

                ["open", file_path]

            )

        else:

            subprocess.call(

                ["xdg-open", file_path]

            )

    except:

        pass


# ======================================================
# OPEN FOLDER
# ======================================================

def open_folder(folder_path):

    try:

        system = platform.system()

        if system == "Windows":

            os.startfile(folder_path)

        elif system == "Darwin":

            subprocess.call(

                ["open", folder_path]

            )

        else:

            subprocess.call(

                ["xdg-open", folder_path]

            )

    except:

        pass


# ======================================================
# COUNT FILES
# ======================================================

def count_files(folder):

    total = 0

    folder = Path(folder)

    if not folder.exists():

        return 0

    for item in folder.rglob("*"):

        if item.is_file():

            total += 1

    return total


# ======================================================
# COUNT FOLDERS
# ======================================================

def count_folders(folder):

    total = 0

    folder = Path(folder)

    if not folder.exists():

        return 0

    for item in folder.rglob("*"):

        if item.is_dir():

            total += 1

    return total


# ======================================================
# HIDDEN FILE
# ======================================================

def is_hidden(file_path):

    return Path(file_path).name.startswith(".")


# ======================================================
# IS FILE
# ======================================================

def is_file(path):

    return Path(path).is_file()


# ======================================================
# IS DIRECTORY
# ======================================================

def is_directory(path):

    return Path(path).is_dir()


# ======================================================
# FILE EXISTS
# ======================================================

def file_exists(path):

    return Path(path).exists()


# ======================================================
# FILE LIST
# ======================================================

def list_files(folder):

    folder = Path(folder)

    files = []

    if not folder.exists():

        return files

    for item in folder.rglob("*"):

        if item.is_file():

            files.append(item)

    return files


# ======================================================
# FOLDER LIST
# ======================================================

def list_folders(folder):

    folder = Path(folder)

    folders = []

    if not folder.exists():

        return folders

    for item in folder.rglob("*"):

        if item.is_dir():

            folders.append(item)

    return folders


# ======================================================
# DELETE EMPTY FOLDERS
# ======================================================

def remove_empty_folders(folder):

    folder = Path(folder)

    removed = 0

    if not folder.exists():

        return removed

    for item in sorted(

        folder.rglob("*"),

        reverse=True

    ):

        if item.is_dir():

            try:

                if len(list(item.iterdir())) == 0:

                    item.rmdir()

                    removed += 1

            except:

                pass

    return removed