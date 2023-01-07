import sys

class System:

    def log(self, message: str) -> None:
        """Prints to the console the current date and time with a message."""
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("{}: {}".format(current_time, message))

    def assertFalse(self, expr, msg=None):
        """Check that the expression is false."""
        if expr:
            self.log(message="{} is not false {}".format(msg, expr))
            sys.exit(1)

    def assertTrue(self, expr, msg=None):
        """Check that the expression is true."""
        if not expr:
            self.log(message="{} is not true {}".format(msg, expr))
            sys.exit(1)

    def readFile(self, file_path: str, mode: str):
        """Read file according to the file path and return a file object,\n
        if the file does not exist it will write a log error message and exit the program.
        """
        try:
            file = open(file_path, mode, errors="ignore")
        except FileNotFoundError:
            self.assertFalse(file is None, "File is not None")
            sys.exit(1)
            
        return file

    def import_docs(self, text_files_path=str):
        """
        Create a list with all the academic text files names and returns it
        :param text_files_path: path of directory with text files
        :return: list with all files name in the directory that represented by text_file_path
        """
        from os import listdir
        from os.path import isfile, join
        files_list = [file for file in listdir(text_files_path) if isfile(join(text_files_path, file))]
        return files_list

    def concat_txt_files(self, list_files_names: list, relative_path: str):
        """
        concate multiple file to one file
        :param list_files_names: list of file names are stored in directory "relative_path"
        :param relative_path: path of directory that contains all the documents
        :return: one big file
        """
        filenames = list_files_names
        with open('Utils/concat_txt_files.txt', 'w') as outfile:
            for fname in filenames:
                with open(relative_path + "" + fname) as infile:
                    for line in infile:
                        outfile.write(line)