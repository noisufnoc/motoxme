import time
import urllib
import httplib
from secrets import APP_TOKEN, USER_KEY
from BeautifulSoup import BeautifulSoup

def pushover_notify(message):
    conn = httplib.HTTPSConnection('api.pushover.net:443')
    conn.request("POST", "/1/messages.json",
                 urllib.urlencode({
                     'token': APP_TOKEN,
                     'user': USER_KEY,
                     'message': message,
                 }), { 'Content-type': 'application/x-www-form-urlencoded' })
    return conn.getresponse()


def check_sale():
    busta = str(time.time()).split('.')[0]

    url = 'http://www.motorola.com/us/shop-all-mobile-phones-1/Moto-X-Developer-Edition-Verizon/moto-x-developer-edition-verizon.html?v=%s' % busta

    resp = urllib.urlopen(url)
    soup = BeautifulSoup(resp)

    price = str(soup('p', 'price')[0]).split('>')[2].split('<')[0]

    if price == '$549.99':
        print 'Not on sale at %s: %s' % (time.strftime("%H:%M:%S", time.localtime()), price)
        return False
        #pushover_notify('Not On Sale: Price is %s' % price)
    else:
        print 'SALE! %s' % price
        pushover_notify('BUY BUY BUY!: Price is %s' % price)
        return True


while check_sale() != True:
    time.sleep(60)
