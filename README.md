# Vacation Decider
This Vacation Decider tool will help you decide where to go on vacation based on historic weather data. This tool is based on airport data by [jpatokal]( https://github.com/jpatokal/openflights) and the temperatures are derived from the [Metaweather API](https://www.metaweather.com/api/). 

## Project structure

```
├── README.md
├── config.yaml
├── requirements.txt
└──  src
     ├── __init__.py
     ├── common.py
     ├── execute.py
     └── tools
        ├── __init__.py
        ├── create_map.py
        └── get_temperatures.py

```


## Setup and Installation

Clone the repository in the directory you want.
```bash
$ git clone git@github.com:sabinescheffer/vacation-decider.git
```

Now create a virtual environment in the root of the project and activate it right away.
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
```
Install the required packages for this tool.
```bash
$ pip install -r requirements.txt
```

## Usage
This tool finds the average temperatures between a start- and enddate for all airports in specific countries. The temperatures are derived from the Metaweather API.
When the temperatures for the chosen countries are fetched, a Folium map will be created and shown in a webbrowser. 

It may take a while to load depending on the amount of airports/dates, you can always check the progress of the load in the log files in your `data` directory. Once the map is loaded, you can click on the coloured dots in the map to see which airport it is and what the average temperature was in you chosen timeframe. 


To edit the countries and timeperiod for which the tool calculates the average temperatures, you can edit the `config.yaml` file.
```bash
$ nano config.yaml
```

To run the tool, enter the following command. A webbrowser will open with the created map.

```bash
$ src/execute.py
```
