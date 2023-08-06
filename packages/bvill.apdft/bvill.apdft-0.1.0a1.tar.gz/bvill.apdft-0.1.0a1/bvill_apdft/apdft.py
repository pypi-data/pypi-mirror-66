"""The primary library module for the apdft project"""

import os
from datetime import datetime
from io import BytesIO
from PyPDF2 import PdfFileMerger
from .utils import get_pdfs_in_dir


def merge(in_paths: list, disable_sorting=False):
    """
    Accepts a list of PDF file paths and returns a BytesIO object containing the
    merged contents of each PDF file.
    """

    merger = PdfFileMerger(strict=False)
    for path in in_paths:
        # fail early if path does not exist, this is already handled by the click
        # library but we want to turn this into an API for other usage as well.
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist!")

        if os.path.isdir(path):
            pdfs_in_dir = get_pdfs_in_dir(path, disable_sorting=disable_sorting)
            for file in pdfs_in_dir:
                print(f"Reading {file}")
                merger.append(file)
        else:
            print(f"Reading {path}")
            merger.append(path)

    file_obj = BytesIO()
    merger.write(file_obj)
    merger.close()
    return file_obj


TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"


def write(file_obj: BytesIO, write_path: str):
    """
    Accepts a file-like object containing PDF content, and a write path
    then writes the object contents to the write path file

    If the write_path is a directory, then a PDF file named with a timestamp
    will be written to the directory instead.

    If the write_path is a directory, this function returns the filename (timestamped)
    of the written file. Otherwise, this function returns None.
    """

    if os.path.isdir(write_path):
        timestamped_file_name = f"{datetime.now():{TIMESTAMP_FORMAT}}.pdf"
        new_file_path = os.path.join(write_path, timestamped_file_name)
        print(f"Writing {new_file_path}")
        with open(new_file_path, "wb") as timestamped_pdf:
            timestamped_pdf.write(file_obj.getbuffer())
        return timestamped_file_name
    else:
        print(f"Writing {write_path}")
        with open(write_path, "wb") as out_pdf:
            out_pdf.write(file_obj.getbuffer())
