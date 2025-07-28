
import logging
import os 
from datetime import datetime


#create logs , directory if it doesnt exist

os.makedirs("logs", exist_ok=True)

#define log filename with timestamp
log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

# Define log format

log_format = "%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s"


#configure logger 

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format=log_format
)

logger =logging.getLogger("real-estate-logger")