import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def map_maker(date_in_mm):

    # zaczytanie bazy danych lotnisk i lotnisk docelowych w dniu wylotu (bez tych 3 dni do przodu)
    database = pd.read_csv('temp_logs/iata-icao.csv')
    dane = pd.read_csv('temp_logs/flights_data.csv')
    dane = dane[dane["data"] == date_in_mm]

    filtered_airports = database[database['iata'].isin(dane['miasto'])]

    # wyznaczanie granic mapy na podstawie minimalnych i maksymalnych wartości szerokości i długości geograficznej
    min_lon = filtered_airports['longitude'].min() - 1
    max_lon = filtered_airports['longitude'].max() + 1
    min_lat = filtered_airports['latitude'].min() - 1
    max_lat = filtered_airports['latitude'].max() + 1

    #tworzenie mapy
    plt.figure(figsize=(12, 8))
    m = Basemap(projection='merc', llcrnrlon=min_lon, urcrnrlon=max_lon, llcrnrlat=min_lat, urcrnrlat=max_lat, resolution='i')

    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.drawmapboundary()

    #punkty lotnisk
    lons = filtered_airports['longitude'].tolist()
    lats = filtered_airports['latitude'].tolist()
    x, y = m(lons, lats)
    m.scatter(x, y, marker='v', color='red', zorder = 5, s = 100)

    #tytuł
    plt.title(f'Możliwe kierunki w dniu {date_in_mm}')

    #zapisuje mape do jpg
    plt.savefig('attachments/mapa_lotnisk.jpg', format='jpg', dpi=300)

