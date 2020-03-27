import os
import sys
import json
import requests
from datetime import datetime

FMT = '%Y-%m-%dT%H:%M'
BASE_URL = "http://apidatos.ree.es/"
category = sys.argv[2]
time_trunc = "hour"
if len(sys.argv) == 1:
    print("Argumentos necesarios")
elif len(sys.argv) == 2:
    url = BASE_URL + sys.argv[1]
elif len(sys.argv) == 4:
    url = BASE_URL + f"{sys.argv[1]}/datos/{category}/{sys.argv[3]}?"


def get_month_data(start_date: datetime, end_date: datetime, year: int, month: int):
    name = os.path.join("datasets",category,f"datos-{category}-{month}-{year}.json")
    if not os.path.isfile(name):
        if not os.path.isdir(os.path.dirname(name)):
            os.mkdir(os.path.dirname(name))  
        _url = url + f"start_date={start_date.strftime(FMT)}&end_date={end_date.strftime(FMT)}&time_trunc={time_trunc}"
        print(f"Haciendo solicitud a {_url}")
        r = requests.get(_url)
        if 'json' in r.headers.get('Content-Type'):
            data = r.json()
            with open(name, "w") as f:
                json.dump(data, f)

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
