#%%
import os
import pandas as pd
from prettytable import PrettyTable
os.chdir("/Users/shanyue/Github/Python_Trip_Project")
from graph_generator import draw_hotel_price, draw_weather
from NLP.nlp_analytics import get_five_top_tourism_attraction, get_word_cloud
from map_generator import get_plan_route
from weather_analysis import city_day_wather
from filter_suitable_service import get_suitable_hotel

#%%
if(__name__ == "__main__"):
    map_detail = pd.read_excel("dataset/map_place_lat_long.xlsx")
    bus_ticket_price = 2
    
    ############################################################
    # Get input from concole
    ############################################################
    print("Input your destination:")
    input_des = input()
    print("Input your travel time down bound: (Format yyyy-mm-dd)")
    input_time_down = input()
    print("Input your travel time up bound: (Format yyyy-mm-dd)")
    input_time_up = input()
    print("Input your hotel money down bound:")
    input_hotel_down = (int)(input())
    print("Input your hotel money up bound:")
    input_hotel_up = (int)(input())
    print("Input your flight money down bound:")
    input_flight_down = (int)(input())
    print("Input your flight money up bound:")
    input_flight_up = (int)(input())
    
    ############################################################
    # Display Hotel Price Information
    ############################################################
    print()
    print()
    print("Hotel Price in "+ input_des)
    draw_hotel_price(input_hotel_down, input_hotel_up, input_des)
    
    ############################################################
    # Display Hotel Weather Information
    ############################################################
    print()
    print()
    print("Weather Information in Line Chart")
    draw_weather(input_time_down, input_time_up, input_des)
    
    print()
    print()
    print("Weather detail:")
    print(city_day_wather(input_des, input_time_down, input_time_up))
    
    ############################################################
    # Display Airline Information
    ############################################################
    print()
    print()
    print("Airline Information in Line Chart")
    draw_weather(input_time_down, input_time_up, input_des)

#%%
    place_list = []
    #airline, air_price = get_suitable_airline(input_des)
    #place_list.append(airline)
    hotel, hotel_price = get_suitable_hotel(input_des)
    place_list.append(hotel)
    tourism_list = get_five_top_tourism_attraction(input_des)
    place_list.extend(tourism_list)
    place_df = pd.DataFrame(place_list,columns=["Place"])
    map_detail["Place"] = map_detail["Place"].str.strip()
    target_spots = pd.merge(place_df,map_detail,on="Place",how="left")
    target_spots = target_spots[~target_spots["Latitude"].isna()]
    
    print("Route plans can be found in map folder:")
    route_plan_list, final_distance = get_plan_route(list(target_spots.values))
    
    ############################################################
    # Display Routes Details
    ############################################################  
    print()
    print()
    print("Route plans detail:")
    for i in range(len(route_plan_list)):
        print("Step "+ str(i+1) + ": " + route_plan_list[i])
    
    ############################################################
    # Display Cost and Distance Information
    ############################################################    
    print()
    print()
    print("Costs and distance")
    table = PrettyTable(["Item", "Money($)"])
    table.add_row(["Hotel", hotel_price])
    #table.add_row(["Airline", air_price])
    table.add_row(["Bus", len(target_spots)/2*bus_ticket_price])
    table.add_row(["Total", hotel_price+len(target_spots)*2])
    print(table)
    
    print("Walking Distance in city: "+ str(final_distance.round(2))+"m")

    ############################################################
    # Display Comments Cloud
    ############################################################
    print()
    print()
    print("Place comments cloud:")
    for spot in tourism_list:
        print(spot)
        get_word_cloud(spot)
        