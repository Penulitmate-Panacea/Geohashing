from bs4 import BeautifulSoup
import urllib.request
soup = BeautifulSoup(urllib.request.urlopen('https://www.marketwatch.com/investing/index/djia').read(),'html.parser')
closingdiv = soup.find_all('td', class_ = 'table__cell u-semi')
closing = closingdiv[0].text.replace(',', '')
#closing = closing.text
print(int(closing))