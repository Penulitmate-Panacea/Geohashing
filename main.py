from datetime import date
from hashlib import md5
from bs4 import BeautifulSoup
from urllib.request import urlopen
soup = BeautifulSoup(urlopen('https://www.marketwatch.com/investing/index/djia').read(),'html.parser')
closingdiv = soup.find_all('td', class_ = 'table__cell u-semi')
lat=int(input("Please enter your current Latitude (nearest whole number)"))
lon=int(input("Please enter your current Longitude(nearest whole number)"))
digest = md5((date.today().strftime("%Y-%m-%d") +"-" +closingdiv[0].text.replace(',', '')).encode('utf-8')).hexdigest()
lat += int(digest[:16],16)/16**16
lon += int(digest[16:],16)/16**16 
print(lat, ", ", lon)