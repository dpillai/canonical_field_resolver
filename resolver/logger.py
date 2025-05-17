import logging

def setup_logger():
    logger = logging.getLogger("FieldResolver")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

logger = setup_logger()
