import time
import urllib
from BeautifulSoup import BeautifulSoup

busta = str(time.time()).split('.')[0]

url = 'http://www.motorola.com/us/shop-all-mobile-phones-1/Moto-X-Developer-Edition-Verizon/moto-x-developer-edition-verizon.html?v=%s' % busta

soup = BeautifulSoup(urllib.urlopen(url))

price = str(soup('p', 'price')[0]).split('>')[2].split('<')[0]

if price == '$549.99':
    print 'NO SALE %s' % price
else:
    print 'SALE! %s' % price

