import os


def handle_file_upload(file, file_upload):

    if not os.path.exists("./uploads"):
        os.makedirs("./uploads")
    with open(f"./uploads/{file_upload.name}", "wb+") as filehandler:
       for chunk in file.chunks():
           filehandler.write(chunk)