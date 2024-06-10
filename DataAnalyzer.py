# Tutaj plik z programem, który analizuje dane

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import MailSender as MS
from datetime import datetime, timedelta
import MapMaker as mp

def analyzer(start_date, receiver, city):
    """ Funkcja, która analizuje dane oraz korzysta z MailSendera do wysłania raportu do usera """

    POLISH_AIRPORTS = {'POZ': 'Poznań',
    'GDN': 'Gdańsk',
    'BZG': 'Bydgoszcz',
    'KTW': 'Katowice',
    'KRK': 'Kraków',
    'LCJ': 'Łódź',
    'LUZ': 'Lublin',
    'RZE': 'Rzeszów',
    'SZY': 'Olsztyn-Mazury',
    'SZZ': 'Szczecin',
    'WAW': 'Warszawa (Chopin)',
    'WRO': 'Wrocław',
    }
    
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

    # Wykres z liczbą lotów w danym dniu:

    title_font_dict = {
        'weight': 'bold',
        'size': 12,
    }
    labels_font_dict = {
    'weight': 'bold'
    }

    x_how_many_flights = [dates[0], dates[1], dates[2], dates[3]]
    y_how_many_flights = [len(first_day), len(second_day), len(third_day), len(fourth_day)]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_how_many_flights, y_how_many_flights, color='lightblue', edgecolor='black', width=0.5)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.xlabel('Data', fontdict=labels_font_dict)
    plt.ylabel('Liczba lotów danego dnia', fontdict=labels_font_dict)
    plt.title(f'Liczba lotów w dniach od {dates[0]} do {dates[3]}', fontdict=title_font_dict)
    plt.grid(axis='y', linestyle='-.', alpha=0.5, linewidth=0.4)
    plt.yticks(range(0, max(y_how_many_flights) + 2, 2))
    plt.margins(x=0.1, y=0.1)
    plt.tight_layout()
    plt.savefig('attachments/figure_one.jpg')

    # Wykres z kosztem minuty lotu

    plt.rcParams["figure.figsize"] = (16, 8)
    figure, axis = plt.subplots(4, 1, sharex=False)
    days = [first_day, second_day, third_day, fourth_day]
    titles = [dates[0], dates[1], dates[2], dates[3]]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for i, ax in enumerate(axis):
        X = days[i]['miasto']
        Y = days[i]['price_time_ratio']
        bars = ax.bar(X, Y, color=colors[i], edgecolor='black')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_title(titles[i], fontsize=14, fontweight='bold', loc='left')
        ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)
        ax.yaxis.set_major_locator(MultipleLocator(2))

    axis[-1].set_xlabel('Destynacja', fontsize=12, fontweight='bold')
    figure.text(0.04, 0.5, 'Koszt minuty lotu [zł]', va='center', rotation='vertical', fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0.04, 0.04, 1, 0.96])
    plt.suptitle(f'Koszt minuty loty w dniach od {dates[0]} do {dates[3]}', fontsize=16, fontweight='bold')
    plt.savefig('attachments/figure_two.jpg')

    # <-- Wybieranie 5 najtanszych kierunkow

    newdf['cena'] = newdf['cena'].astype(int)
    sorted_df = newdf.sort_values(by='cena')
    lowest_prices = sorted_df.iloc[:5]

    x_city = lowest_prices['nazwa_miasta']
    y_price = lowest_prices['cena']
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_city, y_price, color='lightblue', edgecolor='black', width=0.5)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xlabel('Destynacja', fontdict=labels_font_dict)
    plt.ylabel('Cena lotu w złotówkach', fontdict=labels_font_dict)
    plt.title(f'TOP 5 najtańszch kierunków w dniach od {dates[0]} do {dates[3]}', fontdict=title_font_dict)
    plt.grid(axis='y', linestyle='-.', alpha=0.5, linewidth=0.4)
    plt.margins(x=0.1, y=0.1)
    plt.tight_layout()
    plt.savefig('attachments/figure_three.jpg')

    # Generowanie mapy kierunków w danym dniu
    mp.map_maker(start_date)

    # Tworzenie raportu i wysyłanie maila
    attachment_paths = ['attachments/figure_one.jpg', 'attachments/figure_two.jpg','attachments/figure_three.jpg','attachments/mapa_lotnisk.jpg']
    departure_city = POLISH_AIRPORTS[city]
    
    body = MS.content_builder(start_date, end_date, max_price_time_value, min_price_time_value, max_price_time_city, min_price_time_city, most_pop_city, av_price, most_pop_airline, departure_city)

    MS.mail_creator(receiver, body, attachment_paths)
