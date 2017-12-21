# coding=utf-8
"""temporary function definition file, will eventually be different files for better separation of concerns"""


def get_dji_api():
    """"Determine previous closing index of the Dow Jones Industrial Average"""
    import requests
    import datetime
    with open("key1.apikey") as key_file:
        keys = key_file.readlines()
    api_username = keys[0].replace('\n', '')
    api_password = keys[1]
    base_url = "https://api.intrinio.com"
    request_url = base_url + "/prices"
    query_params = {

        'identifier': '$DJI',
        'start_date': datetime.date.today().strftime("%Y-%m-%d"),
        'end_date': datetime.date.today().strftime("%Y-%m-%d")

    }
    response = requests.get(request_url, params=query_params, auth=(api_username, api_password))
    if response.status_code != 200:
        print("API error code: ", response.status_code)
    data = response.json()['data']
    print(data)
    previous_day = data[0]
    return previous_day['close']


def get_dji_scrape():
    """Scrapes today's opening price from Google Finance"""
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    from re import sub
    google_finance = BeautifulSoup(urlopen('https://finance.google.com/finance?cid=983582').read(), 'html.parser')
    snap_table = google_finance.find_all('table', attrs={"class": "snap-data"})
    values = snap_table[0].find_all('td', attrs={"class": "val"})
    opening_row = str(values[2])
    opening_price = sub('[^\d|.]', '', opening_row)
    return opening_price


def get_location():
    """"Determine the user's location using an online service"""
    from requests import get
    from json import loads
    from math import floor
    r = get('http://freegeoip.net/json')
    j = loads(r.text)
    lat = floor(j['latitude'])
    lon = floor(j['longitude'])
    return lat, lon, j


def create_hash(closing):
    """Creates the hash from the users location and closing price of the Dow Jones Industrial Index"""
    from datetime import date
    from hashlib import md5
    pre_hash = date.today().strftime("%Y-%m-%d") + "-" + str(closing)
    digest = md5((pre_hash).encode()).hexdigest()
    lat_add = int(digest[:16], 16) / 16 ** 16
    lon_add = int(digest[16:], 16) / 16 ** 16
    return lat_add, lon_add


def create_goal(home, hash_add):
    """Determines the goal for the geohash"""
    lat_full = home[0] + hash_add[0]
    lon_full = home[1] + hash_add[1]
    lat = round(lat_full, 5)
    lon = round(lon_full, 5)
    return lat, lon


def export_cli(lat, lon, location):
    """Shows the user the goal"""
    print("Your geohash for:", location['city'], ",", location['region_name'], ",", location['country_name'], "is:\n",
          str(lat), ",", str(lon))


def export_map_html(home, result):
    """Saves the starting location and resulting geohash in a html file"""
    from datetime import date
    from folium import Map, Marker, Icon
    try:
        result_map = Map(location=[home[0], home[1]], tiles="Stamen Toner")
        Marker(location=[home[2]['latitude'], home[2]['longitude']], popup='Starting Location',
               icon=Icon(color='green')).add_to(result_map)
        Marker(location=[result[0], result[1]], popup='Geohash Location', icon=Icon(color='red')).add_to(result_map)
        path = ".\Saved\geohash_" + str(date.today().strftime("%Y-%m-%d")) + ".html"
        result_map.save(path)
    except FileNotFoundError:
        from os import mkdir
        mkdir(".\Saved")
        result_map = Map(location=[home[0], home[1]], tiles="Stamen Toner")
        Marker(location=[home[2]['latitude'], home[2]['longitude']], popup='Starting Location',
               icon=Icon(color='green')).add_to(result_map)
        Marker(location=[result[0], result[1]], popup='Geohash Location', icon=Icon(color='red')).add_to(result_map)
        path = ".\Saved\geohash_" + str(date.today().strftime("%Y-%m-%d")) + ".html"
        result_map.save(path)


opening = get_dji_scrape()
start = get_location()
hash_dec = create_hash(opening)
goal = create_goal(start, hash_dec)
export_cli(goal[0], goal[1], start[2])
export_map_html(start, goal)

# TODO 30W fix
# TODO 0001-0930 fix
# TODO allow for historical dates
# TODO confusion matrix testing
# TODO GUI
