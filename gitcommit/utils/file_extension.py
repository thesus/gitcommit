import os


class FileExtension:
    def get_extension(filepath):
        _, ext = os.path.splitext(filepath)
        return ext

    def get_filename(filepath):
        return os.path.basename
