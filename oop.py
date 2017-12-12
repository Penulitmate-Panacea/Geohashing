def scrape():
	from bs4 import BeautifulSoup
	from urllib.request import urlopen
	soup = BeautifulSoup(urlopen('https://www.marketwatch.com/investing/index/djia').read(),'html.parser')#Sticks the webpage into a dataframe
	yesterclosetab = soup.find_all('td', class_ = 'table__cell u-semi')#Finds the table that contains previous days closing index and puts it into a list structure
	yesterclose = yesterclosetab[0].text.replace(',', '')#Changes the table object into a standard string 
	return yesterclose
def get_location():
	from requests import get
	from json import loads
	from math import floor
	r = get('http://freegeoip.net/json')#response for geolocation as a json file
	j = loads(r.text)#load json as string
	lat = floor(j['latitude']) #extract lat from json
	lon = floor(j['longitude'])#extract lon from json	
	return lat, lon,j

def get_hash(closing,lat,lon):
	from datetime import date
	from hashlib import md5
	digest = md5((date.today().strftime("%Y-%m-%d") +"-" +closing).encode('utf-8')).hexdigest()#creates md5 hash digest to modify lat/lon
	latadd = int(digest[:16],16)/16**16#Converts the first  part of the hash to decimal
	lonadd = int(digest[16:],16)/16**16#Converts the second part of the hash to decimal
	return latadd,lonadd

def get_goal(home,hashadd):
	lat = home[0]+hashadd[0] #determines the goal by adding the decimal gained by the hash to the current location
	lon = home[1]+hashadd[1] #determines the goal by adding the decimal gained by the hash to the current location
	return lat,lon	
def export(lat,lon,location):
	print("Your geohash for:", location['city'],",",location['region_name'],",",location['country_name'], "is:\n",str(lat), ",", str(lon))#Prints the resulting destination location
	
def main():	
	closing = scrape()
	home = get_location()
	hashadd = get_hash(closing,home[0],home[1])
	goal = get_goal(home,hashadd)
	export(goal[0],goal[1],home[2])	

main()