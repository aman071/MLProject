import os
import sys
import pandas as pd
from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging

'''
@dataclass:     This is like a special tag that helps create a special kind of class 
                called a "data class." It makes it easier to define a class for holding data.
train_data_path: str = os.path.join('artifacts', 'train.csv'): 
                This line defines an attribute named train_data_path. 
                It's like a spot where you can put the path to your training data file
Data classes are a way to create classes in Python specifically designed to hold data like settings, config, or any kind of information. 
They are useful because they save you from writing a lot of repetitive code.
When you use the @dataclass decorator, Python automatically generates some basic code that you usually need 
when creating classes to hold data. This includes creating an initializer method (like a setup function) that takes the data 
you want to store and sets it up in the class. It also creates a "representation" method that gives you a clear and 
readable way to see what's inside the class when you print it.
If we are only defining variables we can probably use dataclasses. 
If we want to define functions, we should write the general class
'''
'''
Why use dataclasses instead of 
(1)creating global variables
(2)or intializaing the paths inside DataIngestion class itself

1. Structured Configuration: With a @dataclass, you are grouping related configuration variables 
together in a meaningful way. This makes it easier to understand what these settings are for and ensures 
that they are tightly associated with each other.

2. Encapsulation: Using a data class encapsulates your configuration settings within a defined structure. 
This helps avoid polluting the global namespace with multiple configuration variables.

3. Avoiding Global Variables: Creating global variables for configuration can lead to confusion, especially in larger projects. 
Having a dedicated configuration class keeps the configuration localized and easier to manage.

4. Separation of Concerns: By having a separate data class for configuration, you're separating the concerns of handling configuration 
from the actual logic of your DataIngestion class. This can make your codebase more modular and maintainable.

5. Code Organization: Good practice to keep related code together. Grouping configuration settings within a data class improves the organization 
of your code.
'''
@dataclass
class DataIngestionConfig:
    '''
    train_data_path, test_data_path, raw_data_path will be given as input to DataIngestionConfig class
    '''
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()    #this will populate ingest_config with the variables in DataIngestionConfig
    
    def initiate_data_ingestion(self):
        logging.info("Starting data ingestion method")
        try:
            #Read data. Here, reading from csv. Can read from external source like MongoDB also.
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info("Read finished from stud.csv")

            #Make the train directory. Creates the artifacts directory. Without this line, we get an error.
            #Since this is the line which creates the artifacts directory
            #Picks the directory name from train_data_path
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)    #Save csv in raw_path. Just to have everything together

            logging.info('Initiating train_test_split')
            train_set, test_set=train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Data ingestion done')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()