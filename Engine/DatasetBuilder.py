from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProcessor import LinguisticProcessor
from DocVector import DocVector
from joblib import Parallel, delayed
import joblib
import pandas as pd

class DatasetBuilder(System):

    def __init__(self, dir_txt_files_path: str, category:int):

        list_files_names = self.import_docs(dir_txt_files_path)
        self.dataset = self.build(dir_txt_files_path, list_files_names, category)
        
        
    def build(self, dir_txt_files_path: str, list_file_names: str, category:int):
        
        df_list = list()
        for file_name in list_file_names:
            vector = DocVector(doc_path=dir_txt_files_path + "/" + file_name).vector_representation
            vector["Y-LABEL"] = category
            df_list.append(vector)
        return pd.DataFrame.from_records(df_list)
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