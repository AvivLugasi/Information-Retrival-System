from Engine.LinguisticProccessor import LinguisticProccessor
from Utils.System import System


class Tokenizer(System):

    #subclass for store token-poition in current document
    class TokenPosition:
        def __init__(self, token: str, position: int):
            self.token = token
            self.position = position # 0 means non-positional index
        def __str__(self):
            return "token: " + self.token + " | " + "position: " + str(self.position)

    def __init__(self, separators_file: str):
        """Init the Tokenizer class, it reads a separator file and create a list of separators."""
        self.processor = LinguisticProccessor()
        self._separators_list = []
        self.log("Open separators file")
        separators = self.readFile(separators_file, 'r')

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

    def get_SeparatorsList(self):
        """Return the separators list"""
        return self._separators_list

    def tokenize(self, doc: str, is_positional: bool):
        """Create an inverted index from a given file(positional or not positional)"""
        self.log("reading file")
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
                    tokens_list.append(self.TokenPosition(token=token, position=temp_position))
                    # empty the buffer
                    buffer = ""
            else:
                # add char to the buffer
                buffer = buffer + char

        self.log("closing file")
        doc_file.close()

        return tokens_list


tokenizer = Tokenizer("Utils/separetors.txt")
tokens_list = tokenizer.tokenize("../ArtificialIntelligenceExplainability/text/A Bibliometric Analysis of the Explainable Artificial Intelligence Research Fields.txt", True)
# print(dic)
# [print(couple) for couple in dic]
lg = LinguisticProccessor()
lg.linguisticProccessing(tokens_list=tokens_list)