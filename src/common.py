import logging
import logging.config

import os
from os import path

from datetime import datetime, date


def generate_log_structure():
    """Generate logs structure."""

    main_folder = f'data/logs/{date.today()}/'
    if not path.exists(main_folder):
        os.makedirs(main_folder)
    filename = f'{datetime.now()}_logs.txt'
    return main_folder + filename

def setup_logging():
    """logging setup"""
    # Creating and Configuring Logger

    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    filename =  f'data/logs/{date.today()}/{datetime.now()}_logs.txt'
    logging.basicConfig(filename=filename,
                        filemode="w",
                        format=Log_Format,
                        level=logging.INFO)