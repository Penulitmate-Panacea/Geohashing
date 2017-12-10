from datetime import date
from hashlib import md5
from bs4 import BeautifulSoup
from urllib.request import urlopen
soup = BeautifulSoup(urlopen('https://www.marketwatch.com/investing/index/djia').read(),'html.parser')		#Sticks the webpage into a dataframe
closingtab = soup.find_all('td', class_ = 'table__cell u-semi')		#Finds the table that contains previous days closing index and puts it into a list structure
digest = md5((date.today().strftime("%Y-%m-%d") +"-" +closingtab[0].text.replace(',', '')).encode('utf-8')).hexdigest()		#Creates the md5 digest from the top part of the comic
lat=int(input("Please enter your current Latitude (nearest whole number)"))		#Prompt user for their current lattitude
lon=int(input("Please enter your current Longitude(nearest whole number)"))		#Prompt user for their current longitude
lat += int(digest[:16],16)/16**16 		#Converts the first  part of the hash to decimal
lon += int(digest[16:],16)/16**16 		#Converts the second part of the hash to decimal
print(lat, ", ", lon) 					#Prints the resulting destination location