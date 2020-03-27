import json
import copy
import pandas as pd
from numpy import around
from datetime import datetime
from typing import List, Tuple
from scipy.interpolate import InterpolatedUnivariateSpline

FMT = r'%Y-%m-%dT%H:%M:%S.%f%z'

def cleanup(path: str):
    data = json.load(open(path))
    data = data["included"][0]["attributes"]
    def to_24(values: List[Tuple[int, float]]):
        res = []
        def from_25():
            for i in range(0,len(values)-1):
                res.append((i,(values[i][1]+values[i+1][1])/2))
        def from_23():
            x,y = [],[]
            for i,v in values:
                x.append((i*24)/23)
                y.append(v)
            interp = InterpolatedUnivariateSpline(x, y, k=1)
            for i in range(24):
                res.append((i, around(interp(i),1)))
        if len(values)==25:
            from_25()
        if len(values)==23:
            from_23()
        return res
        
    df = pd.DataFrame(data)
    values = df["values"]
    df = df.drop(["values", "description", "color", "type", "magnitude", "composite", "last-update", "title"], axis=1)
    df['value'] = values.apply(lambda x: x['value'])
    df['percentage'] = values.apply(lambda x : x['percentage'])
    df['datetime'] = values.apply(lambda x : datetime.strptime(x['datetime'], FMT))
    max_day = max([x.day for x in df['datetime']])
    n_df = pd.DataFrame()
    for i in (set(df['datetime'].apply(lambda x: x.day))):
        day_df = df[df['datetime'].apply(lambda x: x.day) == i]
        day = [(j//6,day_df['value'][j:j+6].median()) for j in range(0,len(day_df),6)]
        if len(day) != 24:
            day = to_24(day)
        
        n_df = n_df.append([dict(day)], ignore_index = True)
        
    
    return n_df

