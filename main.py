from flask import Flask, render_template, request, url_for
from flask_restful import Api
import definitions as defi
import matplotlib.pyplot as plt

app = Flask(__name__, template_folder='templates')
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Weather_Data_API', methods=['POST'])
def post():
    year = request.form['year']
    month = request.form['month']
    station = request.form['station']

    df1 = defi.import_extract(year, month)
    df = defi.prepare_data(df1)

    one_station = df[df['station name'] == station]

    max = one_station['temp_max'].max()
    min = one_station['temp_min'].min()
    rain = one_station['rainfall'].sum()


    fig, ax = plt.subplots(figsize=(15, 5))
    twin = ax.twinx()

    p1, = ax.plot(
        one_station['day'], one_station['temp_max'],
        color='red',
        label='temp. max',
        alpha=0.5
    )

    p2, = ax.plot(
        one_station['day'], one_station['temp_min'],
        color='blue',
        label='temp. min',
        alpha=0.5
    )

    p3, = ax.plot(
        one_station['day'], one_station['temp_avg'],
        color='grey',
        label='temp. avg',
        alpha=0.5
    )

    p4 = twin.bar(
        x=one_station['day'], height=one_station['rainfall'],
        color='lightgrey',
        label='rainfall',
        alpha=0.5
    )

    ax.axhline(0, c='grey', ls='--')
    ax.set_xlim(0)

    ax.set_title(f'Monthly temperatures in {month}.{year} in {station}', fontsize=14, x=0.16)
    ax.set_xlabel('Day', fontsize=10)
    ax.set_ylabel('Temperature', fontsize=10)
    twin.set_ylabel('Rainfall [mm]', fontsize=10)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(handles=[p1, p2, p3, p4], frameon=False)

    fig1 = plt.gcf()
    fig1.savefig('static/chart.png')
    image_url = url_for('static', filename='chart.png')

    return render_template('Weather_info.html',
                            max=max,
                            min=min,
                            rain=rain,
                            image_url=image_url,
                            station=station)


if __name__ == '__main__':
    app.run(debug=True, port=5252)
