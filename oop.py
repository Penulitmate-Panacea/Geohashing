# coding=utf-8


def api_stock():
    """"Determine the user's location using an online service"""
    from requests import get
    with open("key1.apikey") as key_file:
        keys = key_file.readlines()
        api_username = keys[0].replace('\n', '')
    api_password = keys[1]
    base_url = "https://api.intrinio.com"
    request_url = base_url + "/historical_data"
    query_params = {

        'identifier': '$DJIA',
        'item': 'level',
        'page_size': '1'

    }
    response = get(request_url, params=query_params, auth=(api_username, api_password))
    if response.status_code != 200:
        print("API error code: ", response.status_code)
    data = response.json()['data']
    last_day = data[0]
    return last_day['value']


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


def get_hash(closing):
    """Creates the hash from the users location and closing price of the Dow Jones Industrial Index"""
    from datetime import date
    from hashlib import md5
    digest = md5((date.today().strftime("%Y-%m-%d") + "-" + str(closing)).encode('utf-8')).hexdigest()
    lat_add = int(digest[:16], 16) / 16 ** 16
    lon_add = int(digest[16:], 16) / 16 ** 16
    return lat_add, lon_add


def get_goal(home, hash_add):
    """Determines the goal for the geohash"""
    lat = home[0] + hash_add[0]
    lon = home[1] + hash_add[1]
    return lat, lon


def export(lat, lon, location):
    """Shows the user the goal"""
    print("Your geohash for:", location['city'], ",", location['region_name'], ",", location['country_name'], "is:\n",
          str(lat), ",", str(lon))


last_close = api_stock()
start = get_location()
hash_ = get_hash(last_close)
goal = get_goal(start, hash_)
export(goal[0], goal[1], start[2])
