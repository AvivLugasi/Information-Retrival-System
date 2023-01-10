from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProcessor import LinguisticProcessor
from DocVector import DocVector
from joblib import Parallel, delayed
import joblib
import pandas as pd

class DatasetBuilder(System):

    DIR_FILES_PATH = "../ClassificationModelsDatasets/Category-True"

    def __init__(self, dir_txt_files_path: str, category: int):

        list_files_names = self.import_docs(dir_txt_files_path)
        self.idf_dict = self._idf_dict(dir_files_path=self.DIR_FILES_PATH)
        self.dataset = self.build(dir_txt_files_path, list_files_names, category)

    def build(self, dir_txt_files_path: str, list_file_names: str, category:int):
        
        df_list = list()
        for file_name in list_file_names:
            vector = DocVector(doc_path=dir_txt_files_path + "/" + file_name, idf_dict = self.idf_dict).vector_representation
            vector["Y-LABEL"] = category
            df_list.append(vector)
        return pd.DataFrame.from_records(df_list)
    
    def _idf_dict(self, dir_files_path: str):
        collection_idf_dict = {}
        files_names = self.import_docs(text_files_path=dir_files_path)
        # tokenizer instance
        tokenizer = Tokenizer(separators_file="Utils/separetors.txt")
        # linguistic Processor instance
        lg = LinguisticProcessor()
        for file in files_names:
            # doc = self.read_file(file_path=dir_files_path+ "/" + file, mode='r')
            tokens_dict = tokenizer.tokenize(doc=dir_files_path+ "/" + file)
            doc_terms_dict = lg.preform_processing(tokens_dict=tokens_dict)
            for term in doc_terms_dict.keys():
                if term in collection_idf_dict:
                    collection_idf_dict[term] +=1
                else:
                    collection_idf_dict[term]=1
        # In this point we have (term, df) pairs for all terms in the collection
        for term, df in collection_idf_dict.items():
            print(files_names)
            collection_idf_dict[term]= math.log(df/len(files_names))
        # In this point we have (term, idf) pairs for all terms in the collection
        return collection_idf_dict
# main

# create False category dataset
data_set_false = DatasetBuilder(dir_txt_files_path="../ClassificationModelsDatasets/Category-False", category=0)
data_set_false.dataset.to_csv("../ClassificationModelsDatasets/Category-False-DF.csv")

# create False category dataset
data_set_True = DatasetBuilder(dir_txt_files_path="../ClassificationModelsDatasets/Category-True", category=1)
data_set_True.dataset.to_csv("../ClassificationModelsDatasets/Category-True-DF.csv")
        
# Concatenating the data frames
concatenated_df = pd.concat([data_set_True.dataset,data_set_false.dataset])

# shuffle the data frame
concatenated_df = concatenated_df.sample(frac=1, random_state=1).reset_index()

# remove auto generated extra index column
concatenated_df = concatenated_df.drop('level_0', axis=1)

# save in csv file
concatenated_df.to_csv("../ClassificationModelsDatasets/Concatenated-DF.csv")