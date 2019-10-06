from urllib.request import urlopen  # b_soup_1.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time, timedelta
import pandas as pd

city_name = []
for i in range(3370,3694):
    city_name.append(str(i))

city = {"3370":"Canberra","3372":"Adelaide","3418":"Brisbane","3586":"Melbourne","3677":"Sydney"}

def get_month_list(datestart,dateend):
    month = []
    while datestart<=dateend:
        date_temp = datestart.strftime('%Y-%m')
        if date_temp not in month:
            month.append(date_temp)
        datestart+=timedelta(days=1)
    return month

start = datetime.strptime("2013-11",'%Y-%m')
end = datetime.strptime("2018-5",'%Y-%m')

month = get_month_list(start,end)

writer = pd.ExcelWriter('weather_info.xlsx')
for city_number,city_name in city.items():
    name_list = ['date','start_weather','end_weather','max_temp','min_temp','start_wind','end_wind']
    City = pd.DataFrame(columns=name_list)
    for month_index in month:
        address = "http://www.tianqihoubao.com/guoji/"+city_number+"/"+month_index+".html"
        try:
            html = requests.get(address).content
        except:
            print(address)
            continue
        soup = BeautifulSoup(html,features="html.parser")
        soup2 = soup.findAll('div', class_ = 'wdetail')
        for info in soup2:
            tr_list = info.find_all('tr')[1:]
            for tr in tr_list:
                temp_dict = {}
                td_list = tr.find_all('td')
                temp_dict['date'] = td_list[0].text.strip().replace("\n","")
                temp_dict['start_weather'] = td_list[1].text.strip().replace("\n","").split("/")[0].strip()
                temp_dict['end_weather'] = td_list[1].text.strip().replace("\n","").split("/")[1].strip()
                temp_dict['max_temp'] = td_list[2].text.strip().replace("\n","").split("/")[0].strip()
                temp_dict['min_temp'] = td_list[2].text.strip().replace("\n","").split("/")[1].strip()
                temp_dict['start_wind'] = td_list[3].text.strip().replace("\n","").split("/")[0].strip()
                temp_dict['end_wind'] = td_list[3].text.strip().replace("\n","").split("/")[1].strip()
                City = City.append(temp_dict,ignore_index = True)
    City.to_excel(writer,sheet_name=city_name,index=False,encoding="utf-8")
writer.save()
writer.close()