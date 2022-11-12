from Utils.System import System


class Tokenizer(System):

    def __init__(self, separators_file: str):
        """Init the Tokenizer class, it reads a separator file and create a list of separators."""

        self.separators_list = []
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
                self.separators_list.append(sep)

        self.log("Close separators file")
        separators.close()

    def tokenizeFile(self, doc: str, is_positional: bool):

        self.log("reading file")
        doc_file = self.readFile(doc)
        #TODO create a function to read file char by char and separate words accurding to
        #TODO rules in text_preproccessing.docx
        #if is_positional:
        #    token_dict = dict()
        #    for
        #else:

