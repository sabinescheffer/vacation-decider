#!/usr/bin/env python


import logging

from common import generate_log_structure
from common import setup_logging

from scripts.get_woeids import main as locations_main

generate_log_structure()
setup_logging()
logger = logging.getLogger(__name__)


# Run commands
def main():
    logger.info('---------- RUN STARTING ----------')

    logger.info('---------- LOADING DATA ----------')
    locations_main()

    logger.info('---------- RUN COMPLETED ----------')


if __name__ == '__main__':
    main()
