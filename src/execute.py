#!/usr/bin/env python

import csv
import yaml
import logging

from common import generate_log_structure
from common import setup_logging

from tools.get_temperatures import GetTemperatures

generate_log_structure()
setup_logging()
logger = logging.getLogger(__name__)


# Run commands
def main():
    logger.info('---------- RUN STARTING ----------')

    with open('/Users/sabinescheffer/dev/vacation-decider/config.yaml', 'r') as c:
        config = yaml.load(c, Loader=yaml.FullLoader)

    temperatures = GetTemperatures(config)

    logger.info('---------- LOADING DATA ----------')

    temperatures.create_dataframe().to_csv(
        f"data/temperatures_{config['time_period']['start_date']}_{config['time_period']['end_date']}.csv",
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
        quotechar='"')

    logger.info('---------- LOADING DATA COMPLETED ----------')

    logger.info('---------- RUN COMPLETED ----------')


if __name__ == '__main__':
    main()


