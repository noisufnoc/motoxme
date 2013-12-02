import time
import urllib
import httplib
import logging
from secrets import APP_TOKEN, USER_KEY
from BeautifulSoup import BeautifulSoup

# set some delicious logging
logger = logging.getLogger('xmebro')
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('xmebro.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


def pushover_notify(message):
    conn = httplib.HTTPSConnection('api.pushover.net:443')
    logger.info('Sending %s to Pushover' % message)
    conn.request("POST", "/1/messages.json",
                 urllib.urlencode({
                     'token': APP_TOKEN,
                     'user': USER_KEY,
                     'message': message,
                 }), { 'Content-type': 'application/x-www-form-urlencoded' })
    logger.info('Sent')
    return conn.getresponse()


def check_sale():
    busta = str(time.time()).split('.')[0]

    url = 'http://www.motorola.com/us/shop-all-mobile-phones-1/Moto-X-Developer-Edition-Verizon/moto-x-developer-edition-verizon.html?v=%s' % busta

    logger.info('Checking URL %s' % url)
    resp = urllib.urlopen(url)
    soup = BeautifulSoup(resp)
    logger.info('HTTP Response %s' % str(resp.getcode()))

    price = str(soup('p', 'price')[0]).split('>')[2].split('<')[0]

    if price == '$549.99':
        logger.info('Not on sale at %s: %s' % (time.strftime("%H:%M:%S", time.localtime()), price))
        return False
        #pushover_notify('Not On Sale: Price is %s' % price)
    else:
        logger.info('SALE! %s' % price)
        pushover_notify('BUY BUY BUY!: Price is %s' % price)
        return True


while check_sale() != True:
    time.sleep(60)
    logger.debug('Sleepy...Sleepy...')
