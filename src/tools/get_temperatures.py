#!/usr/bin/env python

import numpy as np
import pandas as pd
import requests
import datetime
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class GetTemperatures:
    """This class is used to load temperatures for airports of the countries/timeframe in the config file"""

    def __init__(self, config):
        """
        Parameters
        ----------
        config : dict
            Configurations that are set in the config.yaml file.
        """

        self.start_date = config['time_period']['start_date']
        self.end_date = config['time_period']['end_date']
        self.countries = config['countries']
        self.airports_url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
        self.weather_url = 'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_mean&timezone=auto'


    def _get_airports_dict(self):
        """Find all airports in the countries given in the config file"""
        print = logger.info

        df = pd.read_csv(self.airports_url, header=None)
        df_filtered = df[df[3].isin(self.countries)][[2, 6, 7]]
        airports = df_filtered.set_index(2).T.to_dict('list')
        return airports

    def _get_temperatures(self):
        print = logger.info
        temp_list = []

        airports = self._get_airports_dict()

        temp_list = []

        for k, v in airports.items():
            response = requests.get(self.weather_url.format(lat=v[0], long=v[1], start_date=self.start_date, end_date=self.end_date))
            items = response.json()

            if 'daily' in items.keys():
                avg_temp = round(np.mean(items['daily']['temperature_2m_mean']), 2)

                temp_list.append({'city': k,
                                  'latt_long': str(v[0]) + ',' + str(v[1]),
                                  'avg_temp': avg_temp})

            print(f'Found temperature for {k}')
        return temp_list

    def create_dataframe(self):
        temp_list = self._get_temperatures()
        df = pd.DataFrame(temp_list)
        df = pd.concat([df, df['latt_long'].str.split(',', expand=True)], axis=1)
        df = df.rename(columns = {0: 'latt', 1: 'long'})
        df = df.drop(columns='latt_long')
        return df
