"""
categories.py
--------------

Contains all supported file categories and helper functions
for detecting the destination folder of a file.

Author : Krishan Kumar
Project : Smart File Organizer
"""

from pathlib import Path

# ==========================================================
# FILE CATEGORIES
# ==========================================================

FILE_CATEGORIES = {

    "Images": {
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".webp", ".svg", ".ico",
        ".tif", ".tiff"
    },

    "Documents": {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".rtf",
        ".odt"
    },

    "Spreadsheets": {
        ".xls",
        ".xlsx",
        ".csv"
    },

    "Presentations": {
        ".ppt",
        ".pptx"
    },

    "Videos": {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".wmv",
        ".flv",
        ".webm"
    },

    "Audio": {
        ".mp3",
        ".wav",
        ".aac",
        ".ogg",
        ".flac",
        ".m4a"
    },

    "Archives": {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz"
    },

    "Python Files": {
        ".py",
        ".ipynb",
        ".pyw"
    },

    "Programming": {

        ".cpp",
        ".c",
        ".java",
        ".js",
        ".ts",
        ".html",
        ".css",
        ".php",
        ".json",
        ".xml",
        ".sql"
    },

    "Executables": {
        ".exe",
        ".msi",
        ".bat",
        ".cmd"
    }

}

# ==========================================================
# RETURN CATEGORY
# ==========================================================

def get_category(file_path):

    extension = Path(file_path).suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "Others"


# ==========================================================
# RETURN ALL CATEGORY NAMES
# ==========================================================

def get_all_categories():

    categories = list(FILE_CATEGORIES.keys())

    categories.append("Others")

    return categories


# ==========================================================
# CHECK CATEGORY
# ==========================================================

def is_supported(extension):

    extension = extension.lower()

    for extensions in FILE_CATEGORIES.values():

        if extension in extensions:
            return True

    return False