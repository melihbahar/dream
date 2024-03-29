import logging

logger = logging.getLogger('training')
my_handler = logging.StreamHandler()
my_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
my_handler.setFormatter(my_formatter)
logger.setLevel(logging.INFO)
logger.addHandler(my_handler)
