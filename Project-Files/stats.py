"""
stats.py
=========================================
Smart File Organizer
Final Version
=========================================
"""

from pathlib import Path
from collections import defaultdict
import os

from categories import get_category
from utils import format_size


class FolderStatistics:

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

    def total_files(self):

        return len(self.files)

    # =====================================================

    def total_folders(self):

        count = 0

        if not self.folder.exists():
            return count

        for item in self.folder.rglob("*"):

            if item.is_dir():
                count += 1

        return count

    # =====================================================

    def total_size(self):

        total = 0

        for file in self.files:

            try:
                total += file.stat().st_size
            except:
                pass

        return format_size(total)

    # =====================================================

    def category_count(self):

        result = defaultdict(int)

        for file in self.files:

            category = get_category(file)

            result[category] += 1

        return dict(result)

    # =====================================================

    def largest_file(self):

        if not self.files:
            return None

        file = max(

            self.files,

            key=lambda f: f.stat().st_size

        )

        return {

            "name": file.name,

            "size": format_size(

                file.stat().st_size

            )

        }

    # =====================================================

    def smallest_file(self):

        if not self.files:
            return None

        file = min(

            self.files,

            key=lambda f: f.stat().st_size

        )

        return {

            "name": file.name,

            "size": format_size(

                file.stat().st_size

            )

        }

    # =====================================================

    def newest_file(self):

        if not self.files:
            return None

        file = max(

            self.files,

            key=lambda f: f.stat().st_mtime

        )

        return {

            "name": file.name,

            "date": file.stat().st_mtime

        }

    # =====================================================

    def oldest_file(self):

        if not self.files:
            return None

        file = min(

            self.files,

            key=lambda f: f.stat().st_mtime

        )

        return {

            "name": file.name,

            "date": file.stat().st_mtime

        }

    # =====================================================

    def average_file_size(self):

        if len(self.files) == 0:
            return "0 B"

        total = 0

        for file in self.files:

            total += file.stat().st_size

        average = total / len(self.files)

        return format_size(average)

    # =====================================================

    def file_types(self):

        result = defaultdict(int)

        for file in self.files:

            result[file.suffix.lower()] += 1

        return dict(result)

    # =====================================================

    def summary(self):

        return {

            "Total Files": self.total_files(),

            "Total Folders": self.total_folders(),

            "Total Size": self.total_size(),

            "Average File Size": self.average_file_size(),

            "Largest File": self.largest_file(),

            "Smallest File": self.smallest_file(),

            "Newest File": self.newest_file(),

            "Oldest File": self.oldest_file(),

            "Categories": self.category_count(),

            "Extensions": self.file_types()

        }

    # =====================================================

    def reset(self):

        self.files.clear()