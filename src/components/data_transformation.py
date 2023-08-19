import sys
import os
import numpy as np
import pandas as pd

from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer_object(self):
        '''
        Responsible for data transformation
        '''
        try:
            #separate out numerical and categorical features because we have to apply different transformations to them
            numerical_features=["writing_score", "reading_score"]
            categorical_features = [
                'gender', 'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            #define pipeline for numerical features
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy="median")),
                    ('standardscaler', StandardScaler(with_mean=False))
                ]
            )

            #define pipeline for categorical features
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            logging.info("num and cat pipelines defined")
            logging.info("num_features:{numerical_features}")
            logging.info("cat_features:{categorical_features}")

            #defining the preprocessor object using the previously defined pipelines
            preprocessor=ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_features), #Pipeline name(can be anything), do this pipeline(variable defined above), on these features
                    ('cat_pipeline', cat_pipeline, categorical_features),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    
    def initiate_data_transformation(self, train_path, test_path):  #This func will receive train_path and test_path
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("read train and test. now getting preprocessor obj")

            #after getting data, get the preprocessor object
            preprocessing_obj=self.get_data_transformer_object()

            target_col='math_score'
            # numerical_features=["writing_score", "reading_score"]

            #make x_train and x_test separating out the features and target
            input_features_train_df=train_df.drop(columns=[target_col], axis=1)
            target_feature_train_df=train_df[target_col]

            input_features_test_df=test_df.drop(columns=[target_col], axis=1)
            target_feature_test_df=test_df[target_col]

            logging.info("training data and target separated")

            #apply the preprocessor pipeline on the data
            input_feature_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocessing_obj.fit_transform(input_features_test_df)

            #concatenate
            train_arr=np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            #concatenate
            test_arr=np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            save_object(    #save_object defined in utils since it is a common func which can be used in many places
                file_path=self.data_transformation_config.preprocessor_obj_file_path,   #file_path obtained from dataclass
                obj=preprocessing_obj    #save this obj in above mentioned file_path
            )

            logging.info("Saved preprocessor obj as pickle file in artifacts/")

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)

