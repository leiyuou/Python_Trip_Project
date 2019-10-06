# -*- coding: utf-8 -*-

import pandas as pd
import os
os.chdir("/Users/shanyue/Github/Python_Trip_Project")


def get_suitable_hotel(city):
    hotel = pd.read_csv("dataset/hotel_data.csv")
    hotel_city = hotel[(hotel["city"]==city) & (hotel["rate"] == "Excellent ")]
    if(len(hotel_city) == 0):
        hotel_city = hotel[(hotel["city"]==city) & (hotel["rate"] == "Very good ")]
    hotel_city = hotel_city.sort_values(by="price", ascending=True)
    return list(hotel_city.iloc[0])[2], list(hotel_city.iloc[0])[6]
    

def get_suitable_airline(city):
    airline = pd.read_csv("dataset/.csv")
    airline_city = airline[(airline["city"]==city) & (airline["rate"] == "Excellent ")]
    if(len(airline_city) == 0):
        airline_city = airline[(airline["city"]==city) & (airline["rate"] == "Very good ")]
    airline_city = airline_city.sort_values(by="price", ascending=True)
    return list(airline_city.iloc[0])


if(__name__=="__main__"):
    suitable_hotel, hotel_price = get_suitable_hotel("Adelaide")
    