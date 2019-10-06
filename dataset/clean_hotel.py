# -*- coding: utf-8 -*-

import pandas as pd
import re

def add_rating(x):
    if(x.startswith("#")):
        rate = re.findall("^#\d+",x)
        return rate[0]
    else:
        return None

hotel = pd.read_excel("hotel_data.xlsx")

hotel["Price"] = hotel["Price"][3:]
hotel["Review"] = hotel["Review"].replace(" reviews","")
hotel["Review"] = hotel["Review"].replace(" review","")
hotel["Review"] = hotel["Review"].replace(",","")
hotel["Rating"] = hotel["Des"].apply(lambda x:add_rating(str(x)))
hotel["Rating"] = hotel["Rating"].str.replace("#","")
hotel["Rating"] = hotel["Rating"].str.replace(" ","")

hotel.to_excel("hotel_data.xlsx",index=False)