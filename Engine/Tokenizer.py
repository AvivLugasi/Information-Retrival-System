from InformationRetrivalSystem.Engine.LinguisticProccessor import Processor
from Utils.System import System


class Tokenizer(System, Processor):

    def __init__(self, separators_file: str):
        """Init the Tokenizer class, it reads a separator file and create a list of separators."""

        self._separators_list = []
        self.log("Open separators file")
        separators = self.readFile(separators_file)

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

    def buildInvertedIndexFromFile(self, doc: str, is_positional: bool):
        """Create an inverted index from a given file(positional or not positional)"""
        self.log("reading file")
        doc_file = self.readFile(doc)
        # terms dict for positional indexing
        terms_dict = dict()
        # terms set for not positional
        terms_set = set()
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
                    # convert the buffer(a token) to a term
                    buffer = self.linguisticProccessing(buffer)
                    if buffer:
                        if is_positional:
                            # insert to the dict
                            position += 1
                            if buffer not in terms_dict:
                                terms_dict[buffer] = list()
                            terms_dict[buffer].append(position)

                        else:
                            # insert to the set
                            terms_set.add(buffer)
                    # empty the buffer
                    buffer = ""
            else:
                # add char to the buffer
                buffer = buffer + char

        self.log("closing file")
        doc_file.close()

        if is_positional:
            return terms_dict
        return terms_set