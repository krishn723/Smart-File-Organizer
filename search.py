"""
search.py
=========================================
Smart File Organizer
Final Version
=========================================
"""

from pathlib import Path
from categories import get_category


class FileSearch:

    def __init__(self, folder):

        self.folder = Path(folder)

        self.files = []

        self.refresh()

    # =====================================================

    def refresh(self):

        self.files.clear()

        if not self.folder.exists():
            return

        for item in self.folder.rglob("*"):

            if item.is_file():

                self.files.append(item)

    # =====================================================

    def get_all_files(self):

        return self.files

    # =====================================================

    def search(self, keyword):

        keyword = keyword.lower().strip()

        if keyword == "":

            return self.files

        results = []

        for file in self.files:

            if keyword in file.name.lower():

                results.append(file)

        return results

    # =====================================================

    def search_extension(self, extension):

        extension = extension.lower()

        if not extension.startswith("."):

            extension = "." + extension

        results = []

        for file in self.files:

            if file.suffix.lower() == extension:

                results.append(file)

        return results

    # =====================================================

    def search_category(self, category):

        if category == "All":

            return self.files

        results = []

        for file in self.files:

            if get_category(file) == category:

                results.append(file)

        return results

    # =====================================================

    def search_multiple(self, keyword="", category="All"):

        keyword = keyword.lower().strip()

        results = []

        for file in self.files:

            if category != "All":

                if get_category(file) != category:

                    continue

            if keyword != "":

                if keyword not in file.name.lower():

                    continue

            results.append(file)

        return results

    # =====================================================

    def total_files(self):

        return len(self.files)

    # =====================================================

    def filenames(self):

        return [

            file.name

            for file in self.files

        ]

    # =====================================================

    def extensions(self):

        ext = set()

        for file in self.files:

            ext.add(file.suffix.lower())

        return sorted(ext)

    # =====================================================

    def categories(self):

        data = {}

        for file in self.files:

            category = get_category(file)

            data.setdefault(category, 0)

            data[category] += 1

        return data

    # =====================================================

    def exists(self, filename):

        for file in self.files:

            if file.name == filename:

                return True

        return False

    # =====================================================

    def get_file(self, filename):

        for file in self.files:

            if file.name == filename:

                return file

        return None

    # =====================================================

    def remove(self, filename):

        self.files = [

            file

            for file in self.files

            if file.name != filename

        ]

    # =====================================================

    def sort_by_name(self):

        self.files.sort(

            key=lambda x: x.name.lower()

        )

    # =====================================================

    def sort_by_size(self):

        self.files.sort(

            key=lambda x: x.stat().st_size

        )

    # =====================================================

    def sort_by_date(self):

        self.files.sort(

            key=lambda x: x.stat().st_mtime

        )

    # =====================================================

    def clear(self):

        self.files.clear()