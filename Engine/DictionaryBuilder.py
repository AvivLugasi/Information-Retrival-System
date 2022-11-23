from Utils.System import System

class DictionaryBuilder(System):

    def __init__(self):
        """...."""
        self.docs = self.import_docs()
        self.dictionary = dict()

    def import_docs(self):
        from os import listdir
        from os.path import isfile, join
        text_files_path = "../ArtificialIntelligenceExplainability/text"
        files_list = [file for file in listdir(text_files_path) if isfile(join(text_files_path, file))]
        return files_list

    

db = DictionaryBuilder()
print(db.docs)
print(len(db.docs))

