import os
import sys
import json
import requests
from datetime import datetime


def download(lang: str, category: str, widget: str):
    assert type(lang) == str, "'lang' tiene que ser string. Consulte https://www.ree.es/es/apidatos"
    assert type(category) == str, "'category' tiene que ser string. Consulte https://www.ree.es/es/apidatos"
    assert type(widget) == str, "'widget' tiene que ser string. Consulte https://www.ree.es/es/apidatos"
    FMT = '%Y-%m-%dT%H:%M'
    BASE_URL = "http://apidatos.ree.es/"
    time_trunc = "hour"
    url = BASE_URL + f"{lang}/datos/{category}/{widget}?"


    def get_month_data(start_date: datetime, end_date: datetime, year: int, month: int):
        name = os.path.join("..","datasets",category,f"datos-{category}-{month}-{year}.json")
        if not os.path.isfile(name):
            if not os.path.isdir(os.path.dirname(name)):
                os.makedirs(os.path.dirname(name))  
            _url = url + f"start_date={start_date.strftime(FMT)}&end_date={end_date.strftime(FMT)}&time_trunc={time_trunc}"
            print(f"Haciendo solicitud a {_url}")
            r = requests.get(_url)
            data = r.json()
            if not 'errors' in data:
                print("Descargando en " + os.getcwd() + os.path.dirname(name))
                with open(name, "w") as f:
                    json.dump(data, f)
            else:
                print("Error en la solicitud a " + _url)

    for year in (2017, 2018, 2019):
        for month in range(1,13):
            start_date = datetime(year,month,1)
            if month == 2:
                end_date = datetime(year, month,28,23,50)
            elif month in (1,3,5,7,8,10,12):
                end_date = datetime(year, month,31,23,50)
            else:
                end_date = datetime(year, month,30,23,50)
            get_month_data(start_date, end_date, year, month)

