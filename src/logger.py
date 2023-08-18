'''
Logging all activity that our application performs.
Done for error handling, etc.
'''

import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #format of log file names
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) #path to log file
os.makedirs(logs_path, exist_ok=True) #Even if file exists, append to it

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH, #create this file
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s", #in this format. this format is best practice
    level=logging.INFO,
)

# Writing main here just to test if logger.py working
# if __name__=="__main__":
#     logging.info("Logging has started")