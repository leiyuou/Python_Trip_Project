#%%
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import os
os.chdir("/Users/shanyue/Github/Python_Trip_Project")
from prettytable import PrettyTable

def check_date(date, begin_date, end_date):
    weather_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    if(weather_date>=begin_date and weather_date<=end_date):
        return 1
    else:
        return 0

def add_price_range(price):
    price=int(price)
    if(price<=100):
        return 0
    elif(price<=200):
        return 1
    elif(price<=300):
        return 2
    elif(price<400):
        return 3
    else:
        return 4

def add_price_range_air(price):
    price=int(price)
    if(price<=500):
        return 0
    elif(price<=600):
        return 1
    elif(price<=700):
        return 2
    elif(price<800):
        return 3
    else:
        return 4

def add_range_hotel(price,hotel_down,hotel_up):
    price = int(price)
    if(price<=(int)(hotel_up) and price>=(int)(hotel_down)):
        return 1
    else:
        return 0

def add_range_air(price,air_down,air_up):
    price = int(price)
    if(price<=(int)(air_up) and price>=(int)(air_down)):
        return 1
    else:
        return 0

def draw_weather(begin_date, end_date, city_name):
    weather_data = pd.read_excel("dataset/weather_data.xlsx",sheet_name=city_name)
    weather_data["date"] = weather_data["date"].str.replace("年","-")
    weather_data["date"] = weather_data["date"].str.replace("月","-")
    weather_data["date"] = weather_data["date"].str.replace("日", "")
    weather_data["within_date"] = weather_data["date"].apply(lambda x:check_date(str(x), begin_date, end_date))
    with_in_weather = weather_data[weather_data["within_date"] == 1]
    plt.plot(with_in_weather["date"].tolist(), with_in_weather["max_temp"].tolist())

    plt.xlabel('date')
    plt.ylabel('max_temp')
    plt.title('Max Temperature')
    plt.yticks([0, 25, 50])
    plt.xticks([])
    plt.show()

def draw_airline(air_down,air_up, city_name):
    airline = pd.read_excel("dataset/airline_data.xlsx")
    airline_city = airline[(airline["ArrivalAirport"].str.contains(city_name))]
    airline_city = airline_city[~airline_city["Price"].isna()]
    airline_city["Price"] = airline_city["Price"].astype(int)
    airline_city["price_within"] = airline_city["Price"].apply(lambda x:add_range_air(x,air_down,air_up))
    airline_city = airline_city[airline_city["price_within"] == 1]
    #airline_city = airline_city.sort_values(by="Price", ascending=True).reset_index(drop=True)
    airline_city["price_range"] = airline_city["Price"].apply(add_price_range_air)
    label_list = ["AU$0-AU$500", "AU$501-AU$600", "AU$601-AU$700", "AU$701-AU$800", ">AU$801"]
    price_size = [len(airline_city[airline_city["price_range"] == 0]), len(airline_city[airline_city["price_range"] == 1]),\
                  len(airline_city[airline_city["price_range"] == 2]),len(airline_city[airline_city["price_range"] == 3]),\
                  len(airline_city[airline_city["price_range"] == 4])]
    explode = [0.05, 0, 0,0,0]
    plt.pie(price_size, explode=explode, labels=label_list, autopct='%1.1f%%', shadow=False, startangle=150)
    plt.title("Airline price pie chart")
    plt.show()
    
    

def draw_hotel_price(hotel_down,hotel_up,city_name):
    hotel_data = pd.read_csv("dataset/hotel_data.csv")
    hotel_data = hotel_data[hotel_data["city"] == city_name]
    hotel_data = hotel_data[~hotel_data["price"].isna()]
    hotel_data["price"] = hotel_data["price"].astype(int)
    hotel_data["price_within"] = hotel_data["price"].apply(lambda x:add_range_hotel(x,hotel_down,hotel_up))
    hotel_data = hotel_data[hotel_data["price_within"] == 1]
    hotel_data["price_range"] = hotel_data["price"].apply(add_price_range)
    label_list = ["AU$0-AU$100", "AU$101-AU$200", "AU$201-AU$300", "AU$301-AU$400", ">AU$401"]
    price_size = [len(hotel_data[hotel_data["price_range"] == 0]), len(hotel_data[hotel_data["price_range"] == 1]),\
                  len(hotel_data[hotel_data["price_range"] == 2]),len(hotel_data[hotel_data["price_range"] == 3]),\
                  len(hotel_data[hotel_data["price_range"] == 4])]
    explode = [0.05, 0, 0,0,0]
    plt.pie(price_size, explode=explode, labels=label_list, autopct='%1.1f%%', shadow=False, startangle=150)
    plt.title("Hotel price pie chart")
    plt.show()

if(__name__ == "__main__"):
    #draw_weather("2014-01-01","2014-04-01","Adelaide")
    draw_hotel_price(100,200,"Adelaide")
