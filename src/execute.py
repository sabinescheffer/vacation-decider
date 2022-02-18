#!/usr/bin/env python
import yaml
import logging
import webbrowser
from flask import Flask

from common import generate_log_structure
from common import setup_logging

from tools.get_temperatures import GetTemperatures
from tools.create_map import CreateMap

generate_log_structure()
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    logger.info('---------- RUN STARTING ----------')

    with open('/Users/sabinescheffer/dev/vacation-decider/config.yaml', 'r') as c:
        config = yaml.load(c, Loader=yaml.FullLoader)

    logger.info('---------- LOADING DATA ----------')

    temperatures = GetTemperatures(config)
    df = temperatures.create_dataframe()

    logger.info('---------- LOADING DATA COMPLETED ----------')

    logger.info('---------- CREATING MAP ----------')

    map = CreateMap(df)
    return map.create_map()

if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True,
            use_reloader=False)

