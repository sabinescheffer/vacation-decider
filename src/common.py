import logging
import logging.config
import os
from datetime import datetime, date
from os import path

import yaml

import logging.config

def generate_log_structure():
    """Generate logs structure."""

    main_folder = f'data/logs/{date.today()}/'
    if not path.exists(main_folder):
        os.makedirs(main_folder)
    filename = f'{datetime.now()}_logs.txt'
    return main_folder + filename

def setup_logging(default_path='logging.yaml', default_level=logging.INFO):
    """logging setup"""

    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print('Failed to load configuration file. Using default configs')