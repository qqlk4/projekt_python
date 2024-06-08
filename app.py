from flask import Flask, render_template, request
import FlightScraper as FS
import pandas as pd
import os
import DataAnalyzer as ds
import matplotlib

matplotlib.use('agg')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/szukaj_tanich_lotow', methods=['GET','POST'])
def szukaj_lotow():
    try:
        if request.method == 'POST':
            dep_airport = request.form.get('departure') # Lotnisko wylotu
            date_in = request.form.get('departureDate') # Data wylotu
            date_out = request.form.get('returnDate') # Data powrotu
            trip_type = request.form.get('tripType') # Czy podroz w jedna czy dwie strony
            mail_owner = request.form.get('mail_sender') # Mail

            if trip_type == 'false':
                flights = FS.azair_oneway(dep_airport, date_in)
                all_flights = FS.azair_oneway_multiple_days(dep_airport, date_in, 3)
                if mail_owner:
                    df = pd.DataFrame(all_flights)
                    df.to_csv('temp_logs/flights_data.csv', index=False)
                    ds.analyzer(date_in, mail_owner,dep_airport)

                return render_template('wyniki_oneway.html', dziennik_lotow=flights)
            elif trip_type == 'true':
                flights = FS.azair_return(dep_airport, date_in, date_out)
                return render_template('wyniki_return.html', dziennik_lotow=flights)
    except:
        if request.method == 'POST':
            return render_template('index_error.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
