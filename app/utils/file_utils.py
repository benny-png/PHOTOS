# app/utils/file_utils.py

import os

def save_uploaded_file(file, directory: str) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_location = os.path.join(directory, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location
