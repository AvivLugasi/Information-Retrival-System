from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProcessor import LinguisticProcessor
# saving dictionary as plk files
from joblib import Parallel, delayed
import joblib
from collections import Counter


class LanguageModel(System):
    TXT_FILES_DIR_PATH = "../ArtificialIntelligenceExplainability/text"

    def __init__(self, after_linguistic_operations: bool, doc_path: str):
        """
        Init a DictionaryBuilder instance
        """
        # # list contains all text docs names in collection
        # self.docs = self._import_docs(text_files_path=self.TXT_FILES_DIR_PATH)
        
        # dictionary: (key=word, value=The probability of the word appearing in the collection)
        self.language_model = self.build(after_linguistic_operations=after_linguistic_operations,
                                         doc_path=doc_path)

    def __str__(self):
        return self.dictionary

    def build(self, after_linguistic_operations: bool, doc_path: str):
        """
        Build the dictionary, can be positional or not.
        :param after_linguistic_operations : build with tokens or terms
        :param doc_path : path to doc file which build a language model for him
        """

        # relative_path = "../ArtificialIntelligenceExplainability/text/"

        # tokenizer instance
        tokenizer = Tokenizer(separators_file="Utils/separetors.txt")
        # linguistic Processor instance
        lg = LinguisticProcessor()

        tokens_dict = tokenizer.tokenize(doc=doc_path)

        words_dict = tokens_dict
        # convert token to terms as demand
        if after_linguistic_operations:
            # extract terms list
            words_dict = lg.preform_processing(tokens_dict=tokens_dict)
        # count how many terms/token exist in the collection
        collection_len = len(words_dict)
        # update the values of the dictionary to be probability instead of tf
        words_dict.update((key, self._calc_prob_for_word(val, collection_len)) for key, val in words_dict.items())

        return words_dict

    ######################################################################################################
    #                                          Helper Functions                                          #
    ######################################################################################################

    def load_dict(self, after_linguistic_operations: bool):
        """Load the dictionary from the pickle file"""
        if after_linguistic_operations:
            self.dictionary = joblib.load('LanguageModels/TokenModel.pkl')
        else:
            self.dictionary = joblib.load('InvertedIndexes/TermModel.pkl')

    def _import_docs(self, text_files_path=str):
        """
        Create a list with all the academic text files names and returns it
        :param text_files_path: path of directory with text files
        """
        from os import listdir
        from os.path import isfile, join
        files_list = [file for file in listdir(text_files_path) if isfile(join(text_files_path, file))]
        return files_list

    def _calc_prob_for_word(self, tf: int, doc_len: int):
        return tf / doc_len


# Main
languageModelByTokens = LanguageModel(after_linguistic_operations=False,
                                      doc_path="../Engine/Utils/concat_txt_files.txt")
languageModelByTerms = LanguageModel(after_linguistic_operations=True, doc_path="../Engine/Utils/concat_txt_files.txt")
print("length of language Model by tokens: " + str(len(languageModelByTokens.language_model)))
print("length of language Model by tokens: " + str(len(languageModelByTerms.language_model)))
print("length of language Model by tokens: " + str(len(languageModelByTokens.language_model)))
print("length of language Model by tokens: " + str(len(languageModelByTerms.language_model)))

counter_model_tokens = Counter(languageModelByTokens.language_model)
print("\nprint top-5 worlds by probability: " + "\n" + counter_model_tokens.most_common(5).__str__())
counter_model_terms = Counter(languageModelByTerms.language_model)
print("\nprint top-5 worlds by probability: " + "\n" + counter_model_terms.most_common(5).__str__())

# lmb.concat_txt_files(list_files_names=lmb.docs, relative_path="../ArtificialIntelligenceExplainability/text/")


# # subclass for a record in a non-positional index in the dictionary
# class DictRecordNonPos:
#     def __init__(self, doc_frequency: int, posting: str):
#         """Init a record instance"""
#         self.doc_frequency = doc_frequency
#         self.postings = set(posting)
#
#     def __str__(self):
#         return "doc frequency: " + str(self.doc_frequency) + " postings: " + str(self.postings)

# # subclass for a record in a positional index in the dictionary
# class DictRecord:
#     def __init__(self, doc_frequency: int, posting: str):
#         """
#         Init a record instance
#         :param doc_frequency: In how many documents does the term appear
#         :param posting: name of document that contains the term
#         """
#         self.doc_frequency = doc_frequency
#         self.postings = dict()
#         self.postings[posting] = list()
#         self.postings[posting].append(position)
#
#     def __str__(self):
#         return "doc frequency: " + str(self.doc_frequency) + " postings: " + str(self.postings)


# # insert each pair into the dictionary
# for pair in terms_list:
#     # if we are creating a positional index
#     if is_positional:
#         # if this is the first occurrence of this term
#         if pair.token not in self.dictionary:
#             pos_record = self.DictRecordPos(doc_frequency=1, posting=file, position=pair.position)
#             self.dictionary[pair.token] = pos_record
#         else:
#             # if this is the first occurrence of this term in specific doc
#             if file not in self.dictionary[pair.token].postings:
#                 self.dictionary[pair.token].doc_frequency += 1
#                 self.dictionary[pair.token].postings[file] = list()
#
#             # add position of the term in the doc list
#             self.dictionary[pair.token].postings[file].append(pair.position)
#     else:
#         # else we are creating a non-positional index
#         # if this is the first occurrence of this term
#         if pair.token not in self.dictionary:
#             non_pos_record = self.DictRecordNonPos(doc_frequency=1, posting=file)
#             self.dictionary[pair.token] = non_pos_record
#         else:
#             # first occurrence of this term in specific doc
#             if file not in self.dictionary[pair.token].postings:
#                 self.dictionary[pair.token].doc_frequency += 1
#                 # add doc name to the set
#                 self.dictionary[pair.token].postings.add(file)


# Main


# build positional dict
# db.buildDict(True)
# keys = db.dictionary.keys()
# db.log("Writing Positional Index to PositionalIndex.txt")
# positional_index_file = db.readFile("InvertedIndexes/PositionalIndex.txt", 'a+')
# for key in keys:
#     positional_index_file.write("Term: " + key + " Postings: " + str(db.dictionary[key]) + "\n")
#
# db.log("Closing PositionalIndex.txt")
# positional_index_file.close()
# db.log("Save Positional Index as a plk file")
# # Save the Positional Index as a pickle in a file
# joblib.dump(db.dictionary, 'InvertedIndexes/PositionalIndex.pkl')
#
# # build non-positional Index
# db.dictionary = dict()
# db.buildDict(False)
# keys = db.dictionary.keys()
# db.log("Writing Non Positional Index to NonPositionalIndex.txt")
# non_positional_index_file = db.readFile("InvertedIndexes/NonPositionalIndex.txt", 'a+')
# for key in keys:
#     non_positional_index_file.write("Term: " + key + " Postings: " + str(db.dictionary[key]) + "\n")
#
# db.log("Closing NonPositionalIndex.txt")
# non_positional_index_file.close()
# db.log("Save Non Positional Index as a plk file")
# # Save the None Positional Index as a pickle in a file
# joblib.dump(db.dictionary, 'InvertedIndexes/NonPositionalIndex.pkl')
