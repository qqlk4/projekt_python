# To jest główny plik ze skrobaczką

from bs4 import BeautifulSoup
import requests as r
from datetime import datetime, timedelta
import pandas as pd


# Dziennik z polskimi lotniskami
POLISH_AIRPORTS = {'POZ': 'Poznan',
'GDN': 'Gdansk',
'BZG': 'Bydgoszcz',
'KTW': 'Katowice',
'KRK': 'Krakow',
'LCJ': 'Lodz',
'LUZ': 'Lublin',
'RZE': 'Rzeszow',
'SZY': 'Olsztyn-Mazury',
'SZZ': 'Szczecin',
'WAW': 'Warsaw',
'WRO': 'Wroclaw',
}

def azair_oneway(iata_code, departure_date, days_ahead=0):
    """ To funkcja, która wykorzystuje azair do wyszukiwania lotów w jedna strone.
    Jako argumenty przyjmuje kod IATA lotniska w Polsce oraz datę wylotu.
    """
    departure_date = (datetime.strptime(departure_date, '%Y-%m-%d') + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    
    # Tutaj niezbędne operacje na stringach, tak by dopasować je do linku
    year = departure_date[0:4]
    if departure_date[5:6] == '0':
        month = departure_date[6:7]
    else:
        month = departure_date[5:7]
    day = departure_date[8:10]

    url_oneway = f'https://www.azair.eu/azfin.php?tp=0&searchtype=flexi&srcAirport={POLISH_AIRPORTS[iata_code]}+%5B{iata_code}%5D&srcTypedText={iata_code.lower()}&srcFreeTypedText=&srcMC=&srcFreeAirport=&dstAirport=Anywhere+%5BXXX%5D&dstTypedText=anywhere&dstFreeTypedText=&dstMC=&adults=1&children=0&infants=0&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&depdate={day}.{month}.{year}&arrdate={day}.{month}.{year}&minDaysStay=1&maxDaysStay=3&nextday=0&autoprice=true&currency=PLN&wizzxclub=false&flyoneclub=false&blueairbenefits=false&megavolotea=false&schengen=false&transfer=false&samedep=true&samearr=true&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&maxChng=0&isOneway=oneway&resultSubmit=Search'

    # Tworzymy skrobaczkę
    request = r.get(url_oneway)
    soup = BeautifulSoup(request.content, 'html.parser')
    
    time = []

    span_time_elements = soup.find_all('span', class_= 'durcha')
    for span_time in span_time_elements:
        time.append(span_time.text[:6])

    flights = []

    div_detail_elements = soup.find_all('div', class_='detail')
    
    # Tutaj mechanizm skrobiący
    id = 0
    for div_detail in div_detail_elements:
        span_to = div_detail.find('span', class_='to')

        if span_to:

            #wyciąganie samej nazwy miasta bez zbędnych śmieci
            full_text = span_to.get_text(separator=' ', strip=True)
            for inner_span in span_to.find_all('span'):
                inner_text = inner_span.get_text(separator=' ', strip=True)
                full_text = full_text.replace(inner_text, '')
            destination_city = ' '.join(full_text.split())

            span_code = span_to.find('span', class_='code')
            current_price = div_detail.find('span', class_='legPrice')
            flight_number = span_to.find('a', title='flightradar24')

            ryanair = div_detail.find('span', class_='airline iataFR')
            wizzair = div_detail.find('span', class_='airline iataW6')
            norwegian = div_detail.find('span', class_='airline iataDY')
            easyJet = div_detail.find('span', class_='airline iataU2')

            if span_code and current_price and ryanair: # Tutaj cos nad tym warunkiem pokminić
                flights.append({'data':departure_date,'nazwa_miasta':destination_city[6:], 'miasto': span_code.text[:3], 'cena': current_price.text, 'czas':time[id] ,'numer_lotu':flight_number.text, 'airline': ryanair.text})
                id +=1
            elif span_code and current_price and wizzair:
                flights.append({'data':departure_date,'nazwa_miasta':destination_city[6:],'miasto': span_code.text[:3], 'cena': current_price.text,'czas':time[id], 'numer_lotu':flight_number.text, 'airline': wizzair.text})
                id +=1
            elif span_code and current_price and norwegian:
                flights.append({'data':departure_date,'nazwa_miasta':destination_city[6:],'miasto': span_code.text[:3], 'cena': current_price.text,'czas':time[id], 'numer_lotu':flight_number.text, 'airline': norwegian.text})
                id +=1
            elif span_code and current_price and easyJet:
                flights.append({'data':departure_date,'nazwa_miasta':destination_city[6:],'miasto': span_code.text[:3], 'cena': current_price.text,'czas':time[id], 'numer_lotu':flight_number.text, 'airline': easyJet.text})
                id +=1
    
    return flights

def azair_oneway_multiple_days(iata_code, departure_date, num_days=3):
    """To funkcja, która zwraca loty na podaną datę oraz na kolejne dni do przodu.
    """
    all_flights = []
    for day in range(num_days + 1):
        flights = azair_oneway(iata_code, departure_date, days_ahead=day)
        all_flights.extend(flights)
    
    
    return all_flights

def azair_return(iata_code, departure_date, arrival_date):
    """ To funkcja, która wykorzystuje azair do wyszukiwania lotów w dwie strony."""

    # Tutaj tez niezbędne operacje na stringach
    year = departure_date[0:4]
    if departure_date[5:6] == '0':
        month = departure_date[6:7]
        ret_zero = '0'
    else:
        month = departure_date[5:7]
    day = departure_date[8:10]


    arr_ret_zero = ''
    arr_year = arrival_date[0:4]
    if arrival_date[5:6] == '0':
        arr_month = arrival_date[6:7]
        arr_ret_zero = '0'
    else:
        arr_month = arrival_date[5:7]
    arr_day = arrival_date[8:10]

    if month == arr_month and year == arr_year:
        arr_day = int(arr_day)
        day = int(day)
        how_many_days = arr_day - day + 1
    elif month != arr_month and int(arr_month)-int(month) < 2 and year == arr_year:
        if int(month)%2 == 0 and month == '02':
            day = 28 - int(day)
        elif int(month)%2 == 0:
            day = 30 - int(day)
        else:
            day = 31 - int(day)

        how_many_days = int(arr_day) + int(day) + 1
        

    url_return = f'https://www.azair.eu/azfin.php?searchtype=flexi&tp=0&isOneway=return&srcAirport={POLISH_AIRPORTS[iata_code]}+%5B{iata_code}%5D&srcFreeAirport=&srcTypedText={iata_code.lower()}&srcFreeTypedText=&srcMC=&dstAirport=Anywhere+%5BXXX%5D&anywhere=true&dstap0=LIN&dstap1=BGY&dstFreeAirport=&dstTypedText=anywhere&dstFreeTypedText=&dstMC=&depmonth={year}{ret_zero}{month}&depdate={departure_date}&aid=0&arrmonth={arr_year}{arr_ret_zero}{arr_month}&arrdate={arrival_date}&minDaysStay={how_many_days}&maxDaysStay={how_many_days}&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&samedep=true&samearr=true&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&autoprice=true&adults=1&children=0&infants=0&maxChng=0&currency=PLN&lang=en&indexSubmit=Search'

    flights = []

    request = r.get(url_return)
    soup = BeautifulSoup(request.content, 'html.parser')

    div_detail_elements = soup.find_all('div', class_='detail')
    prices_to_dest = []

    div_text_elements = soup.find_all('div', class_='text')

    cities = []

    for div_text in div_text_elements:
        span_t = div_text.find('span', class_='to' )
        full_text = span_t.text
        for inner_span in span_t.find_all('span'):
            inner_text = inner_span.get_text(separator=' ', strip=True)
            full_text = full_text.replace(inner_text, '')
        destination_city = ' '.join(full_text.split())
        cities.append(destination_city[6:])
    
    id = 0
    for div_detail in div_detail_elements:

        prices_to_origin = []

        span_to = div_detail.find('span', class_='to')
        if span_to:
            span_code = span_to.find('span', class_='code')
            current_price = div_detail.find('span', class_='legPrice')
            # Co w przypadku, kiedy jest lot jedna linia i powrot inna? Jak sie zachowuje program?
            ryanair = div_detail.find('span', class_='airline iataFR') 
            wizzair = div_detail.find('span', class_='airline iataW6')
            norwegian = div_detail.find('span', class_='airline iataDY')
            easyJet = div_detail.find('span', class_='airline iataU2')

            if span_code and current_price and ryanair:

                actual_price = current_price.text
                actual_price = actual_price.replace(' zł','')
                actual_price = int(actual_price)

                actual_iata = span_code.text

                # Ta czesc kodu odpowiada za sumowanie ceny, by wyswietlac calkowita cene za lot w dwie strony
                if actual_iata != iata_code:
                    prices_to_dest.append(actual_price)
                    dest_iata = span_code.text[:3]

                elif actual_iata == iata_code:
                    prices_to_origin.append(actual_price)

                    total_price = prices_to_dest[0] + prices_to_origin[0]
                    prices_to_dest.clear()

                    flights.append({'nazwa_miasta': cities[id], 'miasto': dest_iata, 'cena': str(total_price)+" zł",'numer_lotu': "", 'airline': ryanair.text})
                    id += 1
            elif span_code and current_price and wizzair:

                actual_price = current_price.text
                actual_price = actual_price.replace(' zł','')
                actual_price = int(actual_price)

                actual_iata = span_code.text

                # Ta czesc kodu odpowiada za sumowanie ceny, by wyswietlac calkowita cene za lot w dwie strony
                if actual_iata != iata_code:
                    prices_to_dest.append(actual_price)
                    dest_iata = span_code.text[:3]

                elif actual_iata == iata_code:
                    prices_to_origin.append(actual_price)

                    total_price = prices_to_dest[0] + prices_to_origin[0]
                    prices_to_dest.clear()
                    flights.append({'nazwa_miasta': cities[id], 'miasto': dest_iata, 'cena': str(total_price)+" zł",'numer_lotu': "", 'airline': wizzair.text})
                    id += 1

            elif span_code and current_price and norwegian:

                actual_price = current_price.text
                actual_price = actual_price.replace(' zł','')
                actual_price = int(actual_price)

                actual_iata = span_code.text

                # Ta czesc kodu odpowiada za sumowanie ceny, by wyswietlac calkowita cene za lot w dwie strony
                if actual_iata != iata_code:
                    prices_to_dest.append(actual_price)
                    dest_iata = span_code.text[:3]

                elif actual_iata == iata_code:
                    prices_to_origin.append(actual_price)

                    total_price = prices_to_dest[0] + prices_to_origin[0]
                    prices_to_dest.clear()
                    flights.append({'nazwa_miasta': cities[id], 'miasto': dest_iata, 'cena': str(total_price)+" zł",'numer_lotu': "", 'airline': norwegian.text})
                    id += 1

            elif span_code and current_price and easyJet:

                actual_price = current_price.text
                actual_price = actual_price.replace(' zł','')
                actual_price = int(actual_price)

                actual_iata = span_code.text[:3]

                # Ta czesc kodu odpowiada za sumowanie ceny, by wyswietlac calkowita cene za lot w dwie strony
                if actual_iata != iata_code:
                    prices_to_dest.append(actual_price)
                    dest_iata = span_code.text[:3]

                elif actual_iata == iata_code:
                    prices_to_origin.append(actual_price)

                    total_price = prices_to_dest[0] + prices_to_origin[0]
                    prices_to_dest.clear()
                    flights.append({'nazwa_miasta': cities[id], 'miasto': dest_iata, 'cena': str(total_price)+" zł",'numer_lotu': "", 'airline': easyJet.text})
                    id += 1

    return flights