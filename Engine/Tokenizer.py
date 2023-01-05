from Utils.System import System


class Tokenizer(System):

    def __init__(self, separators_file: str):
        """Init the Tokenizer class, it reads a separator file and create a list of separators."""
        self._separators_list = []
        # open separators file
        separators = self.readFile(separators_file, 'r')

        # read separators file
        while True:
            # Get next line from file
            line = separators.readline()
            # if line is empty
            # end of file is reached
            if not line:
                break
            for sep in line.split(sep="|"):
                self._separators_list.append(sep)
        separators.close()

    # def get_separators_list(self):
    #     """Return the separators list"""
    #     return self._separators_list

    def tokenize(self, doc: str):
        """
        Create a dictionary from a given file with pairs (token, token frequency)
        :param doc : string represents the path of text file path
        """
        # open text file
        doc_file = self.readFile(doc, 'r')

        # tokens dict (token, token frequency)
        tokens_dict = dict()
        # hold a token
        buffer = ""

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
                    if token in tokens_dict:
                        tokens_dict[token] = tokens_dict[token] + 1
                    else:
                        tokens_dict[token] = 1
                    # empty the buffer
                    buffer = ""
            else:
                # add char to the buffer
                buffer = buffer + char

        # close file
        doc_file.close()

        # return the dictionary of pairs (token, token frequency in the doc)
        return tokens_dict
