
from src.utils.logger import logger
from src.utils.exception import RealEstateException
import sys

def sample_function():
    try:
        logger.info("Starting Sample Function")
        x= 1/0 
    except Exception as e:
        logger.exception("Exceptional Occured")
        raise RealEstateException(str(e), sys)

sample_function()