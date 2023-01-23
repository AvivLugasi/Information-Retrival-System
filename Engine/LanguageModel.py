from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProcessor import LinguisticProcessor
# saving dictionary as plk files
from joblib import Parallel, delayed
import joblib
from collections import Counter


class LanguageModel(System):
    TXT_FILES_DIR_PATH = "../ArtificialIntelligenceExplainability/text"

    def __init__(self):
        """
        Init a DictionaryBuilder instance
        """

        # dictionary: (key=word, value=The probability of the word appearing in the collection)
        #self.language_model = self.build(after_linguistic_operations=after_linguistic_operations,
        #                                 doc_path=doc_path)
        self.language_model = dict()

    def __str__(self):
        return self.dictionary

    def build(self, after_linguistic_operations: bool, doc_path: str):
        """
        Build the dictionary, can be positional or not.
        :param after_linguistic_operations : build with tokens or terms
        :param doc_path : path to doc file which build a language model for him
        """

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
        collection_len = sum(words_dict.values())
        # update the values of the dictionary to be probability instead of tf
        words_dict.update((key, self._calc_prob_for_word(val, collection_len)) for key, val in words_dict.items())

        self.language_model = words_dict

    # ================================================================================================== #
    #                                          Helper Functions                                          #
    # ================================================================================================== #


    def _calc_prob_for_word(self, tf: int, doc_len: int):
        return tf / doc_len


    def load_model(self, after_linguistic_operations: bool):
        """Load the language model from the pickle file"""
        if after_linguistic_operations:
            self.language_model = joblib.load('LanguageModels/languageModelByTokens.pkl')
        else:
            self.language_model = joblib.load('LanguageModels/languageModelByTerms.pkl')


# # Main
# languageModelByTokens = LanguageModel()
# languageModelByTerms = LanguageModel()
#
# languageModelByTokens.build(after_linguistic_operations=False,
#                                       doc_path="../Engine/Utils/concat_txt_files.txt")
# languageModelByTerms.build(after_linguistic_operations=True, doc_path="../Engine/Utils/concat_txt_files.txt")
#
# print("length of language Model by tokens: " + str(len(languageModelByTokens.language_model)))
# print("length of language Model by tokens: " + str(len(languageModelByTerms.language_model)))
# print("length of language Model by tokens: " + str(len(languageModelByTokens.language_model)))
# print("length of language Model by tokens: " + str(len(languageModelByTerms.language_model)))
#
# counter_model_tokens = Counter(languageModelByTokens.language_model)
# print("\nprint top-5 worlds by probability: " + "\n" + counter_model_tokens.most_common(5).__str__())
# counter_model_terms = Counter(languageModelByTerms.language_model)
# print("\nprint top-5 worlds by probability: " + "\n" + counter_model_terms.most_common(5).__str__())
#
# # save both models in pkl files
# print("\nSaving models in LanguageModels/")
# joblib.dump(languageModelByTokens.language_model, 'LanguageModels/languageModelByTokens.pkl')
# joblib.dump(languageModelByTerms.language_model, 'LanguageModels/languageModelByTerms.pkl')
