'''
We will make a web application which will have multiple 
fields, each for entering data for the input
features. Then we submit that data which is caught in the
backend. That data will interact with our preprocessor and model objects
to get predictions to send back.
'''

import sys
from dataclasses import dataclass

import pandas as pd

from src.exception import CustomException
from src.utils import load_object

@dataclass
class PredictPipelineConfig:
    model_path:str = 'artifacts\model.pkl'
    preprocessor_path:str='artifacts\preprocessor.pkl'

class PredictPipeline:
    def __init__(self):
        self.predict_pipeline_paths=PredictPipelineConfig()
    
    def predict(self, features):
        try:
            model=load_object(self.predict_pipeline_paths.model_path)
            preprocessor=load_object(self.predict_pipeline_paths.preprocessor_path)

            scaled_data=preprocessor.transform(features)    #scale features
            pred=model.predict(scaled_data)                 #perform prediction
            return pred
        
        except Exception as e:
            raise CustomException(e,sys)

'''
This class is responsible for mapping the data that we get from frontend
to our backend
'''
class CustomData:
    def __init__(self,
        gender:str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch:str,
        test_preparation_course: str,
        reading_score:int,
        writing_score:int
    ):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score
    
    def get_data_as_df(self):   #return input obtained from user as df
        try:
            custom_input_dict ={
                "gender":[self.gender],
                "race_ethnicity":[self.race_ethnicity],
                "parental_level_of_education":[self.parental_level_of_education],
                "lunch":[self.lunch],
                "test_preparation_course":[self.test_preparation_course],
                "reading_score":[self.reading_score],
                "writing_score":[self.writing_score],
            }

            return pd.DataFrame(custom_input_dict)
        
        except Exception as e:
            raise CustomException(e,sys)
