import logging
import datetime

# Configure the logger hierarchy
logging.getLogger("parent_logger").setLevel(logging.WARNING)
logging.getLogger("parent_logger.child_logger").setLevel(logging.INFO)
logging.getLogger("parent_logger.child_logger.grandchild_logger").setLevel(logging.DEBUG)

# Create a file handler and set its log level
fileHandler = logging.FileHandler(filename=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
fileHandler.setLevel(logging.DEBUG)

# Create a formatter and set it for the file handler
logFormatter = logging.Formatter(
    fmt=f"%(levelname)s %(asctime)s \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler.setFormatter(logFormatter)

# Get an instance of the logger
logger = logging.getLogger("parent_logger.child_logger.grandchild_logger")

# Add the file handler to the logger
logger.addHandler(fileHandler)