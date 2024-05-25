import os


def init_folders():
    dirs = os.listdir()

    if "media" not in dirs:
        os.mkdir("media")


def delete_media():
    files = os.listdir("media/")

    if len(files) > 0:
        for file in files:
            os.remove(f"media/{file}")
