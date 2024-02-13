import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from PIL import Image
from zipfile import ZipFile as zpf
import os
import requests
import savefile

link = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/'
year = '2023'
month = '01'

# open zip folder
def import_extract(year, month):
    zip_url = f'{link}/{year}/{year}_{month}_k.zip'
    filename = f'{year}_{month}_k.zip'
    file = f'k_d_{month}_{year}.csv'
    download_path = f'data/{filename}'
    extracted_path = 'temp'

    try:
        # Download the zip file
        response = requests.get(zip_url)
        with open(download_path, 'wb') as zip_file:
            zip_file.write(response.content)

        with zpf(download_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_path)

        df = pd.read_csv(f'temp/{file}', encoding='unicode_escape', header=None)
        return df

    except Exception as e:
        return f"Error: {str(e)}"

def open_zip(directory, filename: str):
    zip_ref = zpf(f'data/{directory}', 'r')
    zip_ref.extractall('temp')

    file_to_read = os.path.join('temp', filename)

    # Read the file into a DataFrame
    df = pd.read_csv(file_to_read, encoding='unicode_escape', header=None)
    return df


# data preparation
def prepare_data(df_name):
    df_name = df_name.drop(columns=[6, 8, 10, 11, 12, 14, 15, 16, 17])
    header = ['station code', 'station name', 'year', 'month', 'day', 'temp_max', 'temp_min', 'temp_avg', 'rainfall']
    df_name.columns = header
    return df_name


# create chart - it's not working
def create_chart(df_name, station, month, year):
    one_station = df_name[df_name['station name'] == station]

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
    fig1.savefig('output/chart11.png', bbox_inches='tight', dpi=fig.dpi)

    plt.show()

    return print('OK')
