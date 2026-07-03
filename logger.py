"""
logger.py
=========================================
Smart File Organizer
Final Version
=========================================
"""

import logging
from pathlib import Path
from datetime import datetime


class OrganizerLogger:

    def __init__(self):

        self.log_folder = Path("logs")

        self.log_folder.mkdir(

            exist_ok=True

        )

        self.log_file = (

            self.log_folder /

            "organizer.log"

        )

        self.logger = logging.getLogger(

            "SmartFileOrganizer"

        )

        self.logger.setLevel(

            logging.INFO

        )

        if not self.logger.handlers:

            formatter = logging.Formatter(

                "%(asctime)s | %(levelname)s | %(message)s",

                "%d-%m-%Y %H:%M:%S"

            )

            file_handler = logging.FileHandler(

                self.log_file,

                encoding="utf-8"

            )

            file_handler.setFormatter(

                formatter

            )

            self.logger.addHandler(

                file_handler

            )

    # ======================================================

    def info(self,message):

        self.logger.info(message)

    # ======================================================

    def warning(self,message):

        self.logger.warning(message)

    # ======================================================

    def error(self,message):

        self.logger.error(message)

    # ======================================================

    def moved(self,file_name,category):

        self.logger.info(

            f"Moved : {file_name} -> {category}"

        )

    # ======================================================

    def skipped(self,file_name):

        self.logger.warning(

            f"Skipped : {file_name}"

        )

    # ======================================================

    def failed(self,file_name,error):

        self.logger.error(

            f"{file_name} | {error}"

        )

    # ======================================================

    def session_start(self):

        self.logger.info(

            "="*70

        )

        self.logger.info(

            "Organization Started"

        )

    # ======================================================

    def session_end(self):

        self.logger.info(

            "Organization Finished"

        )

        self.logger.info(

            "="*70

        )

    # ======================================================

    def custom(self,message):

        self.logger.info(message)

    # ======================================================

    def delete_log(self):

        try:

            if self.log_file.exists():

                self.log_file.unlink()

        except:

            pass

    # ======================================================

    def log_file_path(self):

        return self.log_file

    # ======================================================

    def current_time(self):

        return datetime.now().strftime(

            "%d-%m-%Y %H:%M:%S"

        )

    # ======================================================

    def separator(self):

        self.logger.info(

            "-"*60

        )

    # ======================================================

    def organization_summary(

        self,

        total,

        moved,

        skipped,

        errors

    ):

        self.separator()

        self.logger.info(

            f"Total Files : {total}"

        )

        self.logger.info(

            f"Moved : {moved}"

        )

        self.logger.info(

            f"Skipped : {skipped}"

        )

        self.logger.info(

            f"Errors : {errors}"

        )

        self.separator()