from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProcessor import LinguisticProcessor
from joblib import Parallel, delayed
import joblib
import math

SEPARATORS_FILES = "Utils/separetors.txt"
LANGUAGE_MODEL_PATH = 'LanguageModels/languageModelByTerms.pkl'

class DocVector(System):

    def __init__(self, doc_path: str, idf_dict: dict):
        # tokenizer instance
        tokenizer = Tokenizer(separators_file=SEPARATORS_FILES)
        # linguistic Processor instance
        lg = LinguisticProcessor()

        self.idf_dict = idf_dict

        tokens_dict = tokenizer.tokenize(doc=doc_path)
        terms_dict = lg.preform_processing(tokens_dict=tokens_dict)

        self.vector_representation = self._build_doc_vector(
            terms_dict=terms_dict)  # { term_appear_in_collection, collection probability * tf in doc}

    # ================================================================================================== #
    #                                          Helper Functions                                          #
    # ================================================================================================== #

    def _build_doc_vector(self, terms_dict: dict):
        """
        This function get terms dictionary and return vector which represent the document.
         A value of a term is normalized tf (in doc input) times idf,
        :param terms_dict: {term, doc_term_frequency}
        :return: vector representation as python dictionary
        """
        # collection_language_model = joblib.load(LANGUAGE_MODEL_PATH)
        # vector = collection_language_model.copy()
        vector = self.idf_dict.copy()
        for term, idf in self.idf_dict.items():
            tf = math.log(terms_dict[term]) if term in terms_dict else 0
            vector[term] = idf * tf
        return vector

# Main

# doc_path="../ArtificialIntelligenceExplainability/text/A_Survey_of_Contrastive_and_Counterfactual_Explanation_Generation_Methods_for_Explainable_Artificial_Intelligence.txt"
# vector_doc = DocVector(doc_path=doc_path)
# print(vector_doc.vector_representation)