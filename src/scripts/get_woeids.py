#!/usr/bin/env python

import yaml
import csv
import logging
import numpy as np
import pandas as pd
import requests
import datetime
from datetime import timedelta

logger = logging.getLogger(__name__)


def get_airports_dict(airports_url, countries):
    df = pd.read_csv(airports_url, header=None)
    df_filtered = df[df[3].isin(countries)]
    airports = df_filtered[[6,7]].to_dict(orient='records')
    return airports

def get_woeid(weather_url, airports_dict):
    locations = {}
    for loc in airports_dict:
        response = requests.get(weather_url + f'search/?lattlong={loc[6]}, {loc[7]}')
        items = response.json()
        if len(items) > 0 and items[0]['distance'] < 10000:
            if items[0]['title'] not in locations.keys():
                locations[items[0]['title']] = {items[0]['latt_long']: items[0]['woeid']}
    return locations

def get_dates(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    dates = [start_date+timedelta(days=x) for x in range(((end_date+timedelta(days=1))-start_date).days)]
    return dates

def get_temperatures(weather_url, locations, dates):
    temp_list = []
    for city, location in locations.items():
        for latt_long, woeid in location.items():
            temp = []
            for day in dates:
                response = requests.get(weather_url + f'{woeid}/{day.year}/{day.month}/{day.day}/')
                items = response.json()
                noon_temp = items[int(len(items)/2)]['the_temp']
                if noon_temp:
                    temp.append(noon_temp)

        temp_list.append({'city': city,
                          'latt_long': latt_long,
                          'avg_temp': round(np.mean(temp),2)})
    return temp_list

def create_dataframe(temp_list):
    df = pd.DataFrame(temp_list)
    df = pd.concat([df, df['latt_long'].str.split(',', expand=True)], axis=1)
    df = df.rename(columns = {0: 'latt', 1: 'long'})
    df = df.drop(columns='latt_long')
    return df

def main():

    with open('/Users/sabinescheffer/dev/vacation-decider/config.yaml', 'r') as c:
        config = yaml.load(c, Loader=yaml.FullLoader)

    start_date = config['time_period']['start_date']
    end_date = config['time_period']['end_date']

    logger.info(f'Find temperatures for countries between {start_date} and {end_date}')

    AIRPORTS_URL = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
    METAWEATHER_URL = 'https://www.metaweather.com/api/location/'

    airports = get_airports_dict(AIRPORTS_URL, config['countries'])
    locations = get_woeid(METAWEATHER_URL, airports)
    dates = get_dates(start_date, end_date)
    temperatures = get_temperatures(METAWEATHER_URL, locations, dates)
    create_dataframe(temperatures).to_csv(f'data/temperatures_{start_date}_{end_date}.csv',
                                          index=False,
                                          quoting=csv.QUOTE_NONNUMERIC,
                                          quotechar='"')

    logger.info(f'Loading temperatures completed')

if __name__ == '__main__':
    main()