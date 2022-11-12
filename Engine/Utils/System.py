class System:

    def log(self, message: str) -> None:
        """Prints to the console the current date and time with a message."""
        import datetime
        courrent_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("{}: {}".format(courrent_time, message))

    def assertFalse(self, expr, msg=None):
        """Check that the expression is false."""
        if expr:
            self.log(message="{} is not false {}".format(msg, expr))
            import sys
            sys.exit(1)

    def assertTrue(self, expr, msg=None):
        """Check that the expression is true."""
        if not expr:
            self.log(message="{} is not true {}".format(msg, expr))
            import sys
            sys.exit(1)

    def readFile(self, file_path: str):
        """Read file according to the file path and return a file object,\n
        if the file does not exist it will write a log error message and exit the program.
        """
        try:
            file = open(file_path, 'r')
        except FileNotFoundError:
            self.assertFalse(file is None, "separators_file is not None")
        return file
