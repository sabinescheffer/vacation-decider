#!/usr/bin/env python
import logging
import folium

logger = logging.getLogger(__name__)

class CreateMap:

    def __init__(self, df):
        self.lat = list(df.latt)
        self.long = list(df.long)
        self.temp = list(df.avg_temp)
        self.cities = list(df.city)

    def _create_colormap(self):
        colormap = folium.LinearColormap(colors=['lightblue', 'orange', 'red'], vmin=min(self.temp), vmax=max(self.temp))
        colormap.caption = 'Average Temperature'
        return colormap

    def _create_map_index(self):
        start_latt_long = (48.5, 4.8)
        folium_map = folium.Map(location=start_latt_long, zoom_start=4)
        return folium_map

    def create_map(self):
        map = self._create_map_index()
        colormap = self._create_colormap()
        print = logger.info
        for loc, city, t in zip(zip(self.lat, self.long), self.cities, self.temp):
            folium.CircleMarker(
                location=loc,
                radius=7,
                popup=(city, t),
                fill=True,
                color=colormap(t),
                fill_opacity=0.8
            ).add_to(map)
            print(f'{city} added to map.')
        colormap.add_to(map)
        return map._repr_html_()
