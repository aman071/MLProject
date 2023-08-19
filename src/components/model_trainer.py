import os
import sys

from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info("Split train and test")
            X_train, y_train, X_test, y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            '''
            After getting training and testing data we define the object for the model we want and fit the data.
            Here, we can see we are defining multiple model objects
            We train multiple models to see which one performs best. This is ok for smaller datasets. But for massive datasets
            we need more planning. Perhaps we can decide which model to use, or we can also take subsets of data and run different
            models on those subsets
            '''
            models={
                'Random Forest':RandomForestRegressor(),
                'Decision Tree':DecisionTreeRegressor(),
                'Grad Boost':GradientBoostingRegressor(),
                'Linear Regression':LinearRegression(),
                'K-neighbors Regressor':KNeighborsRegressor(),
                'XGBRegressor':XGBRegressor(),
                'CatBoost Regressor':CatBoostRegressor(verbose=False),
                'AdaBoost Regressor':AdaBoostRegressor()
            }

            #defining hyperparameters for the above models
            params={
                'Random Forest':    {
                                        'n_estimators':[8,16,32,64,128,256]
                                    },
                

                'Decision Tree':    {
                                        'criterion':['squared_error', 'absolute_error'],
                                    },

                'Grad Boost':       {
                                        'learning_rate':[0.01, 0.05, 0.001],
                                        'subsample':[0.6, 0.7, 0.8, 0.85, 0.9],
                                        'n_estimators':[8, 16, 32, 64, 128, 256]
                                    },

                'Linear Regression':{

                                    },

                'K-neighbors Regressor':    {
                                                'n_neighbors':[5, 7, 9]
                                            },

                'XGBRegressor':     {
                                        'learning_rate':[0.01, 0.05, 0.001],
                                        'n_estimators':[8, 16, 32, 64, 128, 256]
                                    },

                'CatBoost Regressor':{
                                        'depth':[6, 8, 10],
                                        'learning_rate':[0.01, 0.05, 0.001],
                                        'iterations':[30, 50, 100]
                                    },

                'AdaBoost Regressor':{
                                        'learning_rate':[0.01, 0.05, 0.001],
                                        'n_estimators':[8, 16, 32, 64, 128, 256]
                                    },
            }

            #utils.py evaluate_models runs the models and gives us a report on each model
            model_report:dict=evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, 
                                             models=models, params=params)
            
            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model=models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException('Best model <0.6')  
            
            logging.info('Best model found')

            #save the best object obj as pickle dump
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)
            r2_sc=r2_score(y_test,predicted)
            return r2_sc

        except Exception as e:
            raise CustomException(e,sys)
