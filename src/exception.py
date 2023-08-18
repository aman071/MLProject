'''
sys -   provides various functions and variables that are used to manipulate different
        parts of Python runtime environments
'''

import sys
import logging
import os
from src.logger import logging #Instead of below code, we can import logging from logger

#Without this exception was being raised but log file was not being created
# logs_directory = "logs"
# os.makedirs(logs_directory, exist_ok=True)
# logging.basicConfig(
#     filename=os.path.join(logs_directory, "error.log"),  # Specify the name of the log file
#     format="[%(asctime)s] %(levelname)s - %(message)s",  # Define the log message format
#     level=logging.INFO  # Set the logging level to INFO or higher
# )

# error_detail would come sys
def error_message_detail(error, error_detail:sys):
    _,_, exc_tb=error_detail.exc_info() #error details
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_msg="Error occurred in python script [{0}], line number [{1}], error message [{2}]".format(
        file_name,exc_tb.tb_lineno, str(error)
    )
    return error_msg

#Custom exception class, inheriting from Exception
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message


# Writing main here just to test if exception.py working
# if __name__=="__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("DivideByZero error")
#         raise CustomException(e, sys)