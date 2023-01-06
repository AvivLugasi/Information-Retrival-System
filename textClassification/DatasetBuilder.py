from Utils.System import System
from Tokenizer import Tokenizer
from LinguisticProcessor import LinguisticProcessor
import DocVector
from joblib import Parallel, delayed
import joblib


class DatasetBuilder(System):

    def __init__(self, dir_txt_files_path: str):

        list_files_names = self.import_docs(dir_txt_files_path)
        self.dataset = build(dir_txt_files_path, list_files_names)
        
        
    def build(self, dir_txt_files_path: str, list_file_names: str):
        
        df = 
        for file_name in list_file_names:
            vector = DocVector(doc_path=dir_txt_files_path + "" + file_name).vector_representation
            


        

