from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProccessor import LinguisticProccessor

class DictionaryBuilder(System):

    def __init__(self):
        """Init a DictionaryBuilder instance"""
        # text docs names
        self.docs = self.import_docs()
        # dictionary
        self.dictionary = dict()
        # tokenizer instance
        self.tokenizer = Tokenizer("Utils/separetors.txt")
        # linguistic Processor instance
        self.lg = LinguisticProccessor()

    def import_docs(self):
        """Create a list with all the academic text files names and returns it"""
        from os import listdir
        from os.path import isfile, join
        text_files_path = "../ArtificialIntelligenceExplainability/text"
        files_list = [file for file in listdir(text_files_path) if isfile(join(text_files_path, file))]
        return files_list

    

db = DictionaryBuilder()
relative_path = "../ArtificialIntelligenceExplainability/text/"
for file in db.docs:
    tokens_list = db.tokenizer.tokenize(relative_path + file, True)
    terms_list = db.lg.linguisticProccessing(tokens_list=tokens_list)
    print("{} token list".format(file))
    for pair in terms_list:
        print(pair)

