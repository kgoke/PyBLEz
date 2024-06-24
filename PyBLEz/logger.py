import logging

# Configure the logger
logger = logging.getLogger("PyBLEz")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler = logging.StreamHandler()   
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)  
logger.setLevel(logging.WARNING) # default to warniung to avoid verbose output

def enable_logs():
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled")

def disable_logs():
    logger.setLevel(logging.CRITICAL)
    logger.debug("Logging disabled")     