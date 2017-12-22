# coding=utf-8
"""Handles backend of data collection process, note all functions should not be passed parameters"""


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
