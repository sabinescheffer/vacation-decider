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
        self.weather_url = 'https://www.metaweather.com/api/location/'


    def _get_airports_dict(self):
        """Find all airports in the countries given in the config file"""

        df = pd.read_csv(self.airports_url, header=None)
        df_filtered = df[df[3].isin(self.countries)]
        airports = df_filtered[[6,7]].to_dict(orient='records')
        return airports

    def _get_woeid(self):
        print = logger.info
        locations = {}
        airports_dict = self._get_airports_dict()

        for loc in airports_dict:
            response = requests.get(self.weather_url + f'search/?lattlong={loc[6]}, {loc[7]}')
            items = response.json()
            if len(items) > 0 and items[0]['distance'] < 10000:
                if items[0]['title'] not in locations.keys():
                    locations[items[0]['title']] = {items[0]['latt_long']: items[0]['woeid']}
                    print(f"Found latt/long for airport of {items[0]['title']}")
        return locations

    def _get_dates(self):
        start_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(self.end_date, "%Y-%m-%d")
        dates = [start_date+timedelta(days=x) for x in range(((end_date+timedelta(days=1))-start_date).days)]
        return dates

    def _get_temperatures(self):
        print = logger.info
        temp_list = []

        locations = self._get_woeid()
        dates = self._get_dates()

        for city, location in locations.items():
            for latt_long, woeid in location.items():
                temp = []
                for day in dates:
                    response = requests.get(self.weather_url + f'{woeid}/{day.year}/{day.month}/{day.day}/')
                    items = response.json()
                    noon_temp = items[int(len(items)/2)]['the_temp']
                    if noon_temp:
                        temp.append(noon_temp)

            temp_list.append({'city': city,
                              'latt_long': latt_long,
                              'avg_temp': round(np.mean(temp),2)})
            print(f'Found temperature for {city}')
        return temp_list

    def create_dataframe(self):
        temp_list = self._get_temperatures()
        df = pd.DataFrame(temp_list)
        df = pd.concat([df, df['latt_long'].str.split(',', expand=True)], axis=1)
        df = df.rename(columns = {0: 'latt', 1: 'long'})
        df = df.drop(columns='latt_long')
        return df
