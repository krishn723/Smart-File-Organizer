"""
organizer.py
=========================================
Smart File Organizer
Final Version
=========================================
"""

import shutil
from pathlib import Path

from categories import get_category
from utils import get_unique_filename


class FileOrganizer:

    def __init__(self, folder):

        self.folder = Path(folder)

        self.total_files = 0
        self.moved_files = 0
        self.skipped_files = 0
        self.error_files = 0

        self.activity = []

    # =====================================================

    def scan_files(self):

        files = []

        if not self.folder.exists():

            return files

        for item in self.folder.iterdir():

            if item.is_file():

                files.append(item)

        return files

    # =====================================================

    def organize(

        self,

        progress_callback=None,

        log_callback=None

    ):

        files = self.scan_files()

        self.total_files = len(files)

        if self.total_files == 0:

            return self.summary()

        for index, file in enumerate(files, start=1):

            try:

                category = get_category(file)

                destination_folder = (

                    self.folder /

                    category

                )

                destination_folder.mkdir(

                    exist_ok=True

                )

                destination = get_unique_filename(

                    destination_folder,

                    file.name

                )

                shutil.move(

                    str(file),

                    str(destination)

                )

                self.moved_files += 1

                message = (

                    f"Moved : "

                    f"{file.name}"

                    f" -> "

                    f"{category}"

                )

                self.activity.append(message)

                if log_callback:

                    log_callback(message)

            except Exception as e:

                self.error_files += 1

                message = (

                    f"Error : "

                    f"{file.name}"

                    f" ({e})"

                )

                self.activity.append(message)

                if log_callback:

                    log_callback(message)

            finally:

                progress = int(

                    (

                        index /

                        self.total_files

                    ) * 100

                )

                if progress_callback:

                    progress_callback(progress)

        return self.summary()

    # =====================================================

    def summary(self):

        return {

            "Total Files": self.total_files,

            "Moved": self.moved_files,

            "Skipped": self.skipped_files,

            "Errors": self.error_files

        }

    # =====================================================

    def get_activity(self):

        return self.activity

    # =====================================================

    def reset(self):

        self.total_files = 0

        self.moved_files = 0

        self.skipped_files = 0

        self.error_files = 0

        self.activity.clear()