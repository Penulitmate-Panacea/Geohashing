from datetime import date
from hashlib import md5
from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests import get
from json import loads
soup = BeautifulSoup(urlopen('https://www.marketwatch.com/investing/index/djia').read(),'html.parser')#Sticks the webpage into a dataframe
closingtab = soup.find_all('td', class_ = 'table__cell u-semi')#Finds the table that contains previous days closing index and puts it into a list structure
digest = md5((date.today().strftime("%Y-%m-%d") +"-" +closingtab[0].text.replace(',', '')).encode('utf-8')).hexdigest()#Creates the md5 digest from the top part of the comic
r = get('http://freegeoip.net/json')#response for geolocation as a json file
j = loads(r.text)#load json as string
lat = j['latitude']# extract lat from json
lon = j['longitude']#extract lon from json
lat += int(digest[:16],16)/16**16#Converts the first  part of the hash to decimal
lon += int(digest[16:],16)/16**16#Converts the second part of the hash to decimal
print(lat, ",", lon)#Prints the resulting destination location