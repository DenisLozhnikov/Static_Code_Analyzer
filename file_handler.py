import os
import glob


class FileHandler:
    def __init__(self, path):
        self.path = path

    def get_filter_files(self, extension=None):
        """
        Get all files in given path if path - directory, otherwise path will be returned
        :param extension: files with specified extension will be returned
        :return: all files within directory
        """
        if os.path.isfile(self.path):
            return [self.path]
        os.chdir(self.path)
        return [self.path + '\\' + file for file in glob.glob("**/*." + extension, recursive=True)]
