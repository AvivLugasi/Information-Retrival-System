from LinguisticProccessor import LinguisticProccessor
from Utils.System import System


class Tokenizer(System):

    def __init__(self, separators_file: str):
        """Init the Tokenizer class, it reads a separator file and create a list of separators."""
        self.processor = LinguisticProccessor()
        self._separators_list = []
        # open separators file
        self.log("Open separators file")
        separators = self.readFile(separators_file, 'r')

        # read separators file
        while True:
            # Get next line from file
            line = separators.readline()
            self.log("Read line from separators files")
            # if line is empty
            # end of file is reached
            if not line:
                break
            for sep in line.split(sep="|"):
                self._separators_list.append(sep)

        self.log("Close separators file")
        separators.close()

    #subclass for store token-position in current document
    class TokenPosition:

        def __init__(self, token: str, position: int):
            """Init a TokenPosition instance"""
            self.token = token
            self.position = position # 0 means non-positional index
        def __str__(self):
            return "token: " + self.token + " | " + "position: " + str(self.position)

    def get_SeparatorsList(self):
        """Return the separators list"""
        return self._separators_list

    def tokenize(self, doc: str, is_positional: bool):
        """Create an inverted index from a given file(positional or not positional)"""
        # open text file
        self.log("Reading {}".format(doc))
        doc_file = self.readFile(doc, 'r')

        # terms dict for positional indexing
        tokens_list = []
        # hold a token
        buffer = ""
        # position in the file
        position = 0

        # loop the chars in the file
        while True:
            # read char
            char = doc_file.read(1)
            # if we reached EOF
            if not char:
                break
            # if we reached a separator
            if char in self._separators_list:
                # if buffer not empty
                if buffer != "":
                    token = buffer
                    position += 1
                    temp_position = position if is_positional else 0
                    # add a token position pair to the list
                    tokens_list.append(self.TokenPosition(token=token, position=temp_position))
                    # empty the buffer
                    buffer = ""
            else:
                # add char to the buffer
                buffer = buffer + char

        # close file
        self.log("Closing {}".format(doc))
        doc_file.close()

        # return the token position pairs list
        return tokens_list