# Import the logging module to create log messages
import logging
import os
from datetime import datetime


# Create a log file name based on the current date and time.
# Example: 07_27_2026_21_35_1753632310.log
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# Create the path where the log folder will be created.
# os.getcwd() returns the current working directory.
#
# Example:
# Current Directory:
# D:\Projects\ML_Project
#
# logs_path becomes:
# D:\Projects\ML_Project\logs\07_27_2026_21_35_1753632310.log
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)


# Create the directory if it doesn't already exist.
#
# exist_ok=True means:
# If the directory already exists, don't raise an error.
os.makedirs(logs_path, exist_ok=True)


# Create the complete path of the log file.
#
# Example:
# D:\Projects\ML_Project\logs\07_27_2026_21_35_1753632310.log\
# 07_27_2026_21_35_1753632310.log
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


# Configure the logging system
logging.basicConfig(

    # File where logs will be stored
    filename=LOG_FILE_PATH,

    # Format of each log message
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",

    # Log only INFO and above
    level=logging.INFO,
)