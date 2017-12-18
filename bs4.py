# coding=utf-8
#Legacy webscrape
from bs4 import BeautifulSoup
from urllib.request import urlopen
soup = BeautifulSoup(urlopen('http://www.marketwatch.com/investing/index/djia').read(), 'html.parser')
yesterclosetab = soup.find_all('td', class__='table__cell u-semi')
print("var:", yesterclosetab)  # debugging
print("type:", type(yesterclosetab))  # debugging options
yesterclose = yesterclosetab[0].text.replace(',', '')  # Changes the table object into a standard string
