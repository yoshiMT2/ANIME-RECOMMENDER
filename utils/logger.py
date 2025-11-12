import logging
import os
from datetime import datetime

LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOGS_DIR,
    'log_{date_str}.log'.format(
        date_str=datetime.now().strftime('%Y-%m-%d')
    )
)

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s %(message)s',
    level=logging.INFO
)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger
