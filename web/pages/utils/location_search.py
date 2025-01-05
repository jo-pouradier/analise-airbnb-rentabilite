import os
import pandas as pd
import math

data_path1 = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'pondered_listings_process.csv')
listings_data = pd.read_csv(data_path1)

data_path2 = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'loyer_process.csv')
loyer_data = pd.read_csv(data_path2)
loyer_data['latitude'] = loyer_data['geo_point_2d'].apply(lambda x: float(x.split(',')[0]))
loyer_data['longitude'] = loyer_data['geo_point_2d'].apply(lambda x: float(x.split(',')[1]))

print(listings_data.shape)
print(loyer_data.shape)


def location_search(lat, long, distance):
    """
    return all listings and loyer data within a certain distance from a given location
    :param lat:
    :param lon:
    :return:
    """
    lat_max_distance = (distance / 1000 / 111.32)
    long_max_distance = (distance / 1000 / (40075 * math.cos(math.radians(lat)) / 360))
    listings_search = listings_data.loc[abs(listings_data['latitude'] - lat) <= lat_max_distance].loc[
        abs(listings_data['longitude'] - long) <= long_max_distance]
    loyer_search = loyer_data.loc[abs(loyer_data['latitude'] - lat) <= lat_max_distance].loc[
        abs(loyer_data['longitude'] - long) <= long_max_distance]
    return listings_search, loyer_search


if __name__ == '__main__':
    listings_search, loyer_search = location_search(48.8566, 2.3522, 100)

    print(listings_search.shape)
    print(loyer_search.shape)
