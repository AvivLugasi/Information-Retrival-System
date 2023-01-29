from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProcessor import LinguisticProcessor
from DocVector import DocVector
from joblib import Parallel, delayed
import joblib
import pandas as pd
import math

class DatasetBuilder(System):

    def __init__(self, collection_file_paths: list, dir_txt_files_path: str=None, category=None):
        if dir_txt_files_path is not None:
            list_files_names = self.import_docs(dir_txt_files_path)
        self.idf_dict = self._idf_dict(dir_files_paths=collection_file_paths)
        if category is not None:
            self.dataset = self.build(dir_txt_files_path, list_files_names, category)

    def build(self, dir_txt_files_path: str, list_files_names: str, category:int):
        
        df_list = list()
        for file_name in list_files_names:
            vector = DocVector(doc_path=dir_txt_files_path + "/" + file_name, idf_dict = self.idf_dict).vector_representation
            vector["Y-LABEL"] = category
            df_list.append(vector)
        return pd.DataFrame.from_records(df_list)
    
    def _idf_dict(self, dir_files_paths: list):
        collection_idf_dict = {}
        #files_names = self.import_docs(text_files_path=dir_files_path)
        # tokenizer instance
        tokenizer = Tokenizer(separators_file="Utils/separetors.txt")
        num_of_files = 0
        # linguistic Processor instance
        lg = LinguisticProcessor()
        for path in dir_files_paths:
            files_names = self.import_docs(text_files_path=path)
            num_of_files += len(files_names)
            for file in files_names:
                # doc = self.read_file(file_path=dir_files_path+ "/" + file, mode='r')
                tokens_dict = tokenizer.tokenize(doc=path + "/" + file)
                doc_terms_dict = lg.preform_processing(tokens_dict=tokens_dict)
                for term in doc_terms_dict.keys():
                    if term in collection_idf_dict:
                        collection_idf_dict[term] +=1
                    else:
                        collection_idf_dict[term]=1

        # In this point we have (term, df) pairs for all terms in the collection
        print(max(collection_idf_dict.values()))
        print(min(collection_idf_dict.values()))
        for term, df in collection_idf_dict.items():
            collection_idf_dict[term]= math.log(num_of_files/df)
        # In this point we have (term, idf) pairs for all terms in the collection
        return collection_idf_dict
