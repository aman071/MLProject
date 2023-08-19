'''
Any functionalities common to entire application 
will be present here.
'''

import os
import sys
import dill

import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report={}

        #for each model
        for i in range(len(list(models))):
            model=list(models.values())[i]  #get the model object
            param=params[list(models.keys())[i]]

            gs=GridSearchCV(model, param, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)     #fit data using that model

            #get predictions on training data
            y_train_pred=model.predict(X_train)
            train_score=r2_score(y_train, y_train_pred)

            #get predictions on testing data
            y_test_pred=model.predict(X_test)
            test_score=r2_score(y_test, y_test_pred)

            #add test score as model report
            report[list(models.keys())[i]]=test_score

        return report
    
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)