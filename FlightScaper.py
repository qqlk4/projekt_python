# Główny plik ze skrobaczką -- to tutaj znajdują się wszystkkie funkcje itd..
# COMMITUJMY tylko jak mamy coś konkretnego, tak to pracujmy lokalnie, zeby nie zaśmiecać

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# Uniwersalne
departure_airport = 'GDN'
date_in = '2024-04-12'
date_out = '2024-04-14'
destination = 'ARN'

# Dla Wizzair
is_return_wizz_yes, is_return_wizz_no = 'roundtrip', 'oneway'

# Dla Ryanair
is_return_ryr_no, is_return_ryr_yes = 'false', 'true' # or 'true' zmienic na value jesli podroz w dwie strony

# RYANAIR
# Podroz w dwie strony
URL_RYR = f'https://www.ryanair.com/pl/pl/cheap-flights-beta?originIata={departure_airport}&dateOut={date_in}&dateIn={date_out}&isExactDate=true&destinationIata=ANY&isReturn={is_return_ryr_yes}&isMacDestination=false&promoCode=&adults=1&teens=0&children=0&infants=0&outboundFromHour=00:00&outboundToHour=23:59&inboundFromHour=00:00&inboundToHour=23:59&priceValueTo=&currency=PLN&isFlexibleDay=false'

URL_WIZZ = f'https://www.esky.pl/flights/select/{is_return_wizz_yes}/ap/{departure_airport}/ap/{destination}?departureDate={date_in}&returnDate={date_out}&pa=1&py=0&pc=0&pi=0&sc=economy&eventSource=Filter&filter%5Bairline%5D=W6&page=1&filter%5Bno-multiline%5D=YES'

URL_WIZZ_ONEWAY = f'https://www.esky.pl/flights/select/{is_return_ryr_no}/ap/{departure_airport}/ap/{destination}?departureDate={date_in}&pa=1&py=0&pc=0&pi=0&sc=economy&eventSource=Filter&page=1&filter%5Bairline%5D=W6'

# W9 --> Wizz Air UK (POZ, Bydzia, LUBLIN, ) ; W6 - Wizz Air

options = Options()
options.add_argument('--headless') # To powoduje, ze okno przegladarki sie nie odpala, tylko dziala "w tle"

driver = webdriver.Firefox(options=options)

def wizz_scraper():
    """ Funkcja pobiera i zwraca dane na temat cen i destynacji """