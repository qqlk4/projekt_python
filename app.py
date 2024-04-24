from flask import Flask, render_template, request
import FlightScraper as FS

# Zrobić coś jak strona sie wypierdala! --> Tzn jakieś ładne "Ops, we're sorry"
# Zrobić coś, jak strona się ładuje, zeby to ladnie wyglądało

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/szukaj_tanich_lotow', methods=['GET','POST'])
def szukaj_lotow():
    if request.method == 'POST':
        dep_airport = request.form.get('departure') # Lotnisko wylotu
        date_in = request.form.get('departureDate') # Data wylotu
        date_out = request.form.get('returnDate') # Data powrotu
        trip_type = request.form.get('tripType') # Czy podroz w jedna czy dwie strony

        if trip_type == 'false':
            flights = FS.azair_oneway(dep_airport, date_in)
        elif trip_type == 'true':
            flights = FS.azair_return(dep_airport, date_in, date_out)
    return render_template('wyniki.html', dziennik_lotow=flights)


if __name__ == '__main__':
    app.run(port=8000, debug=True)