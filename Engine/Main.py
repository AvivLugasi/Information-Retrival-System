import pandas as pd
from DatasetBuilder import DatasetBuilder
from Utils.System import System
from Tokenizer import Tokenizer
from LanguageModel import LanguageModel
from LinguisticProcessor import LinguisticProcessor
# saving dictionary as plk files
from joblib import Parallel, delayed
import joblib


# Task 1
languageModelByTokens = LanguageModel()
languageModelByTerms = LanguageModel()

languageModelByTokens.build(after_linguistic_operations=False,
                                      doc_path="Utils/concat_txt_files.txt")
languageModelByTerms.build(after_linguistic_operations=True, doc_path="Utils/concat_txt_files.txt")

# save both models in pkl files
print("\nSaving models in LanguageModels/")
joblib.dump(languageModelByTokens.language_model, 'LanguageModels/languageModelByTokens.pkl')
joblib.dump(languageModelByTerms.language_model, 'LanguageModels/languageModelByTerms.pkl')

# Task 2
# create False category dataset
data_set_false = DatasetBuilder(dir_txt_files_path="../ClassificationModelsDatasets/Category-False", category=0, collection_file_path="../ClassificationModelsDatasets/Category-True")
data_set_false.dataset.to_csv("../ClassificationModelsDatasets/Category-False-DF.csv")

# create False category dataset
data_set_True = DatasetBuilder(dir_txt_files_path="../ClassificationModelsDatasets/Category-True", category=1, collection_file_path="../ClassificationModelsDatasets/Category-True")
data_set_True.dataset.to_csv("../ClassificationModelsDatasets/Category-True-DF.csv")

# Concatenating the data frames
concatenated_df = pd.concat([data_set_True.dataset, data_set_false.dataset])

# shuffle the data frame
concatenated_df = concatenated_df.sample(frac=1, random_state=1).reset_index()

# remove auto generated extra index column
concatenated_df = concatenated_df.drop('level_0', axis=1)

# save in csv file
concatenated_df.to_csv("../ClassificationModelsDatasets/Concatenated-DF.csv")