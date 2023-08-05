import logging
import os
import sys

__version__ = '0.0.1'

# toolbox 
ROOT_DIR = os.environ.get('CB_ROOT', os.path.abspath('..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# logging
LEVEL = logging.DEBUG if os.environ.get('DEBUG') else logging.INFO
LOG_FILE = os.path.join(ROOT_DIR, 'logs/log.log')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# get a default logger to the project
logger = logging.getLogger(__name__)
logger.setLevel(LEVEL)

# make this log send messages to stdout
output = logging.StreamHandler(sys.stdout)
#os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
#output = logging.FileHandler(LOG_FILE)
output.setLevel(LEVEL)
output.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(output)