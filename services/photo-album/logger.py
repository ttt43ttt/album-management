import logging

def create_logger(logfilename):
    """Create logger for logging to screen and file."""

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfilename)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s\n%(message)s", "%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Also print log messages to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
