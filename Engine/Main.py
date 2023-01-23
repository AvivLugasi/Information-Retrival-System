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
data_set_false = DatasetBuilder(dir_txt_files_path="../ClassificationModelsDatasets/Category-False", category=0,
                                collection_file_paths=["../ClassificationModelsDatasets/Category-True"])
data_set_false.dataset.to_csv("../ClassificationModelsDatasets/Category-False-DF.csv")

# create False category dataset
data_set_True = DatasetBuilder(dir_txt_files_path="../ClassificationModelsDatasets/Category-True", category=1,
                               collection_file_paths=["../ClassificationModelsDatasets/Category-True"])
data_set_True.dataset.to_csv("../ClassificationModelsDatasets/Category-True-DF.csv")

# Concatenating the data frames
concatenated_df = pd.concat([data_set_True.dataset, data_set_false.dataset])

# shuffle the data frame
concatenated_df = concatenated_df.sample(frac=1, random_state=1).reset_index()

# remove auto generated extra index column
concatenated_df = concatenated_df.drop('level_0', axis=1)

# save in csv file
concatenated_df.to_csv("../ClassificationModelsDatasets/Concatenated-DF.csv")

# Task 3
# create vectors representations for clustering task
dataset_builder = DatasetBuilder(collection_file_paths=["../ArtificialIntelligenceExplainability/text", "../ClusteringDocs/AlgorithmicFairness"\
                                                        , "../ClusteringDocs/FilterBubble", "../ClusteringDocs/GenderBias"])

dataset_ArtificialIntelligenceExplainability = dataset_builder.build(dir_txt_files_path="../ArtificialIntelligenceExplainability/text",\
                                                                     list_files_names=dataset_builder.import_docs("../ArtificialIntelligenceExplainability/text"),\
                                                                     category="ArtificialIntelligenceExplainability")
dataset_AlgorithmicFairness = dataset_builder.build(dir_txt_files_path="../ClusteringDocs/AlgorithmicFairness",\
                                                                     list_files_names=dataset_builder.import_docs("../ClusteringDocs/AlgorithmicFairness"),\
                                                                     category="AlgorithmicFairness")
dataset_FilterBubble = dataset_builder.build(dir_txt_files_path="../ClusteringDocs/FilterBubble",\
                                                                     list_files_names=dataset_builder.import_docs("../ClusteringDocs/FilterBubble"),\
                                                                     category="FilterBubble")
dataset_GenderBias = dataset_builder.build(dir_txt_files_path="../ClusteringDocs/GenderBias",\
                                                                     list_files_names=dataset_builder.import_docs("../ClusteringDocs/GenderBias"),\
                                                                     category="GenderBias")
# Concatenating the data frames
concatenated_df = pd.concat([dataset_ArtificialIntelligenceExplainability,
                             dataset_AlgorithmicFairness, dataset_FilterBubble, dataset_GenderBias])

# shuffle the data frame
concatenated_df = concatenated_df.sample(frac=1, random_state=1).reset_index()

# remove auto generated extra index column
concatenated_df = concatenated_df.drop('level_0', axis=1)

# save in csv file
concatenated_df.to_csv("../ClusteringDocs/Concatenated-DF.csv")