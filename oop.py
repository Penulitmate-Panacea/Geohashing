def scrape():
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    soup = BeautifulSoup(urlopen('http://www.marketwatch.com/investing/index/djia').read(),'html.parser')
    #print(soup)
    yesterclosetab = soup.find_all('td', class__='table__cell u-semi')
    print("var:",yesterclosetab)
    yesterclose = yesterclosetab[0].text.replace(',', '')  # Changes the table object into a standard string
    return yesterclose


def get_location():
    from requests import get
    from json import loads
    from math import floor
    r = get('http://freegeoip.net/json')  # response for geolocation as a json file
    j = loads(r.text)  # load json as string
    lat = floor(j['latitude'])  # extract lat from json
    lon = floor(j['longitude'])  # extract lon from json
    return lat, lon, j


def get_hash(closing):
    from datetime import date
    from hashlib import md5
    digest = md5((date.today().strftime("%Y-%m-%d") + "-" + closing).encode('utf-8')).hexdigest()
    lat_add = int(digest[:16], 16) / 16 ** 16  # Converts the first  part of the hash to decimal
    lon_add = int(digest[16:], 16) / 16 ** 16  # Converts the second part of the hash to decimal
    return lat_add, lon_add


def get_goal(home, hash_add):
    lat = home[0] + hash_add[0]  # determines the goal by adding the decimal gained by the hash to the current location
    lon = home[1] + hash_add[1]  # determines the goal by adding the decimal gained by the hash to the current location
    return lat, lon


def export(lat, lon, location):
    print("Your geohash for:", location['city'], ",", location['region_name'], ",", location['country_name'], "is:\n",
          str(lat), ",", str(lon))  # Prints the resulting destination location


def main():
    closing = scrape()
    home = get_location()
    hash_ = get_hash(closing)
    goal = get_goal(home, hash_)
    export(goal[0], goal[1], home[2])


def debug():
    import argparse
    import logging

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

def codecfix():
    import sys
    import codecs
    if sys.stdout.encoding != 'cp850':
      sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'cp850':
      sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'strict')


debug()
codecfix()
main()
