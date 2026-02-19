import logging
import os
from datetime import datetime

import traceback

# Create Logs folder to log information / steps
LOG_DIR = os.path.join(os.getcwd(),"logs")
os.makedirs(LOG_DIR, exist_ok=True)


class Logger:

    _logger_initialized = False

    @classmethod
    def _initialize_logger(cls):
        
        if cls._logger_initialized:
            return
        
        ## Create logger, set level as info
        logger = logging.getLogger("FrameworkLogger")
        logger.setLevel(logging.INFO)

        ## set logging format
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # console transport
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


        # App Log file
        app_log_file = os.path.join(LOG_DIR,"app.log")
        file_handler = logging.FileHandler(app_log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        #Error Log file
        error_log_file = os.path.join(LOG_DIR,'error.log')
        error_handler = logging.FileHandler(error_log_file)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

        cls._logger_initialized = True

    @classmethod
    def info(cls, message:str):
        cls._initialize_logger()
        logging.getLogger("FrameworkLogger").info(message)

    @classmethod
    def warn(cls, message:str):
        cls._initialize_logger()
        logging.getLogger('FrameworkLogger').warning(message)

    @classmethod
    def error(cls, message:str, error: Exception = None):
        cls._initialize_logger()
        logger = logging.getLogger('FrameworkLogger')

        if error:
            logger.error(f"{message}\n{traceback.format_exc}")
        else:
            logger.error(message)


    @classmethod
    def log_error(cls, class_name:str, method_name:str, exception:Exception):
        cls._initialize_logger()
        logger = logging.getLogger("FrameworkLogger")
        logger.error(f"ClassName: {class_name}")
        logger.error(f"MethodName: {method_name}")
        logger.error(f"Exception: {traceback.format_exc()}")
        logger.error("-" * 60)

