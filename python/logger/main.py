import logging

import init_logger


def log_an_error():
    log = logging.getLogger(__name__)
    log.error("Uh oh, something's not right")


if __name__ == '__main__':
    init_logger.setup()
    logging.info("Wow, that was simple...")
    log_an_error()
