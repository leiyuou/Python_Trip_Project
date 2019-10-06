import time
from datetime import datetime, date, time
import pandas as pd
import os
os.chdir("/Users/shanyue/Github/Python_Trip_Project")

def city_day_wather(city,start,end):
    start = start.replace("-","")[-4:]
    end = end.replace("-","")[-4:]
    City = pd.read_excel('dataset/weather_data.xlsx', sheet_name=city)
    date_index = City.iloc[:, 0].tolist()
    City.index = City.iloc[:, 0]

    City_date_index = []
    for i in date_index:
        t = i.split("年");
        if t[1] not in City_date_index:
            City_date_index.append(t[1])

    City_Weather = pd.DataFrame(index=City_date_index, columns=["min_temp", "max_temp"])
    for i in City_date_index:
        min = 0
        max = 0
        length = 0
        for j in date_index:
            if i in j and "1"+i not in j:
                min_temp = City.loc[j]['min_temp']
                max_temp = City.loc[j]['max_temp']
                try:
                    if (len(min_temp.split("℃")) == 2):
                        min_temp = min_temp.split("℃")
                    else:
                        min_temp = min_temp.split("°C")
                    if (len(max_temp.split("℃")) == 2):
                        max_temp = max_temp.split("℃")
                    else:
                        max_temp = max_temp.split("°C")
                except:
                    continue

                min += int(min_temp[0])
                max += int(max_temp[0])
                length += 1
        City_Weather.loc[i]["min_temp"] = min / length
        City_Weather.loc[i]["max_temp"] = max / length
    new_index = []
    for i in City_Weather.index:
        month = i.split("月")[0]
        date = i.split("月")[1].split("日")[0]
        if (len(month) == 1):
            if (len(date) == 1):
                new_index.append("0" + month + "0" + date)
            else:
                new_index.append("0" + month + date)
        elif (len(date) == 1):
            new_index.append(month + "0" + date)
        else:
            new_index.append(month + date)
    City_Weather.index = new_index
    return City_Weather.sort_index().loc[start:end]
