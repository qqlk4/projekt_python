# Tutaj plik z programem, który analizuje dane

# To co mozna zrobić:
# --> Gdzie mozna poleciec w danym przedziale cenowym
# --> Mapa z połączeniami 

import pandas as pd
import matplotlib.pyplot as plt
import MailSender as MS
from datetime import datetime, timedelta

def analyzer(start_date, receiver):
    """ Funkcja, która analizuje dane oraz korzysta z MailSendera do wysłania raportu do usera """
    
    # Wczytywanie danych
    data_path = 'temp_logs/flights_data.csv'
    data = pd.read_csv(data_path)
    df = pd.DataFrame(data=data)


    # Data cleaning 
    newdf = df.drop(['numer_lotu'], axis=1)
    newdf['czas'] = newdf['czas'].str.replace(' h','')
    newdf['cena'] = newdf['cena'].str.replace(' zł','')

    # Funkcja do generowania zakresu dat
    def generate_date_list(start_date_in):
        start_date = datetime.strptime(start_date_in, '%Y-%m-%d')
        date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4)]
        
        return date_list
    dates = generate_date_list(start_date)
    end_date = dates[3]

    # Obliczanie średniej ceny biletu lotniczego
    newdf['cena'] = pd.to_numeric(newdf['cena'], errors='coerce')
    av_price = round(newdf['cena'].mean(),2)

    # Do ktorego miasta loty są najczęściej?
    most_pop_city = newdf['nazwa_miasta'].value_counts().index[0]

    # Najpopularniejsza linia lotnicza
    most_pop_airline = newdf['airline'].value_counts().index[0]


    # Przeliczanie ile kosztuje minuta lotu
    newdf['price_time_ratio'] = 0.0
    for x in range(len(newdf)):
        price = int(newdf['cena'][x])
        time = newdf['czas'][x]
        hours_to_minutes = int(time[0])*60
        minutes = int(time[2:4])
        total_time_in_minutes = hours_to_minutes + minutes
        price_to_time_ratio = round(price/total_time_in_minutes,2)

        newdf.at[x, 'price_time_ratio'] = price_to_time_ratio


    max_price_time_value = newdf['price_time_ratio'].max()
    max_price_time = newdf[newdf['price_time_ratio'] == max_price_time_value]
    max_price_time_city = max_price_time['nazwa_miasta'].iloc[0]


    min_price_time_value = newdf['price_time_ratio'].min()
    min_price_time = newdf[newdf['price_time_ratio'] == min_price_time_value]
    min_price_time_city = min_price_time['nazwa_miasta'].iloc[0]

    # Ilość lotow danego dnia 
    first_day = newdf[newdf['data'] == dates[0]]
    second_day = newdf[newdf['data'] == dates[1]]
    third_day = newdf[newdf['data'] == dates[2]]
    fourth_day = newdf[newdf['data'] == dates[3]]

    # <-- Pobawić się nad stylami wykresow
    x_how_many_flights = [dates[0], dates[1], dates[2], dates[3]]
    y_how_many_flights = [len(first_day), len(second_day), len(third_day), len(fourth_day)]
    plt.bar(x_how_many_flights, y_how_many_flights)
    plt.xlabel('Data')
    plt.ylabel('Ilość lotów danego dnia')
    plt.title(f'Ilość lotów w dniach od {dates[0]} do {dates[3]}')
    plt.savefig('attachments/figure_one.jpg')

    # <-- Pobawić się nad stylami wykresow

    plt.rcParams["figure.figsize"] = (16,8)
    figure, axis = plt.subplots(4)

    X = first_day['miasto']
    Y = first_day['price_time_ratio']
    axis[0].bar(X,Y)

    X = second_day['miasto']
    Y = second_day['price_time_ratio']
    axis[1].bar(X,Y)

    X = third_day['miasto']
    Y = third_day['price_time_ratio']
    axis[2].bar(X,Y)

    X = fourth_day['miasto']
    Y = fourth_day['price_time_ratio']
    axis[3].bar(X,Y)
    plt.savefig('attachments/figure_two.jpg')

    # Tworzenie raportu i wysyłanie maila
    attachment_paths = ['attachments/figure_one.jpg', 'attachments/figure_two.jpg']
    
    body = MS.content_builder(start_date, end_date, max_price_time_value, min_price_time_value, max_price_time_city, min_price_time_city, most_pop_city, av_price, most_pop_airline)

    MS.mail_creator(receiver, body, attachment_paths)