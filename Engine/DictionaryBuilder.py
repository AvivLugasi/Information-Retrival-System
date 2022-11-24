from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProccessor import LinguisticProccessor
#saving dictionary as plk files
from joblib import Parallel, delayed
import joblib

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

    def __str__(self):
        return self.dictionary

    def loadDict(self, is_positional: bool):
        """Load the dictionary from the pickle file"""
        if is_positional:
            self.dictionary = joblib.load('PositionalIndex.pkl')
        else:
            self.dictionary = joblib.load('NonPositionalIndex.pkl')

    # subclass for a record in a non-positional index in the dictionary
    class DictRecordNonPos:
        def __init__(self, doc_frequency: int, posting: str):
            """Init a record instance"""
            self.doc_frequency = doc_frequency
            self.postings = set(posting)

        def __str__(self):
            return "doc frequency: " + str(self.doc_frequency) + " postings: " + str(self.postings)

    # subclass for a record in a positional index in the dictionary
    class DictRecordPos:
        def __init__(self, doc_frequency: int, posting: str, position: int):
            """Init a record instance"""
            self.doc_frequency = doc_frequency
            self.postings = dict()
            self.postings[posting] = list()
            self.postings[posting].append(position)

        def __str__(self):
            return "doc frequency: " + str(self.doc_frequency) + " postings: " + str(self.postings)

    def import_docs(self):
        """Create a list with all the academic text files names and returns it"""
        from os import listdir
        from os.path import isfile, join
        text_files_path = "../ArtificialIntelligenceExplainability/text"
        files_list = [file for file in listdir(text_files_path) if isfile(join(text_files_path, file))]
        return files_list

    def buildDict(self, is_positional: bool):
        """Build the dictionary, can be positional or not."""
        relative_path = "../ArtificialIntelligenceExplainability/text/"
        # loop text docs
        for file in self.docs:
            # extract tokens list
            tokens_list = self.tokenizer.tokenize(relative_path + file, is_positional)
            # extract terms list
            terms_list = self.lg.linguisticProccessing(tokens_list=tokens_list)
            # insert each pair into the dictionary
            for pair in terms_list:
                # if we are creating a positional index
                if is_positional:
                    # if this is the first occurrence of this term
                    if pair.token not in self.dictionary:
                        pos_record = self.DictRecordPos(doc_frequency= 1, posting= file, position= pair.position)
                        self.dictionary[pair.token] = pos_record
                    else:
                        # if this is the first occurrence of this term in specific doc
                        if file not in self.dictionary[pair.token].postings:
                            self.dictionary[pair.token].doc_frequency += 1
                            self.dictionary[pair.token].postings[file] = list()

                        # add position of the term in the doc list
                        self.dictionary[pair.token].postings[file].append(pair.position)
                else:
                    # else we are creating a non-positional index
                    # if this is the first occurrence of this term
                    if pair.token not in self.dictionary:
                        non_pos_record = self.DictRecordNonPos(doc_frequency= 1, posting= file)
                        self.dictionary[pair.token] = non_pos_record
                    else:
                        # first occurrence of this term in specific doc
                        if file not in self.dictionary[pair.token].postings:
                            self.dictionary[pair.token].doc_frequency += 1
                            # add doc name to the set
                            self.dictionary[pair.token].postings.add(file)

# Main
db = DictionaryBuilder()
# build positional dict
db.buildDict(True)
keys = db.dictionary.keys()
db.log("Writing Positional Index to PositionalIndex.txt")
positional_index_file = db.readFile("PositionalIndex.txt", 'a+')
for key in keys:
    positional_index_file.write("Term: " + key + " Postings: " +  str(db.dictionary[key]) + "\n")

db.log("Closing PositionalIndex.txt")
positional_index_file.close()
db.log("Save Positional Index as a plk file")
# Save the Positional Index as a pickle in a file
joblib.dump(db.dictionary, 'PositionalIndex.pkl')

# build non-positional Index
db.dictionary = dict()
db.buildDict(False)
keys = db.dictionary.keys()
db.log("Writing Non Positional Index to NonPositionalIndex.txt")
non_positional_index_file = db.readFile("NonPositionalIndex.txt", 'a+')
for key in keys:
    non_positional_index_file.write("Term: " + key + " Postings: " +  str(db.dictionary[key]) + "\n")

db.log("Closing NonPositionalIndex.txt")
non_positional_index_file.close()
db.log("Save Non Positional Index as a plk file")
# Save the None Positional Index as a pickle in a file
joblib.dump(db.dictionary, 'NonPositionalIndex.pkl')
