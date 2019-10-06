#%%
import os
os.chdir("/Users/shanyue/Github/Python_Trip_Project")
from project_deliver.graph_generator import draw_hotel_price, draw_weather


# with open("AdelaideMetroStops_geojson/AdelaideMetroStops_GDA94.geojson") as file:
#     line_list = file.readlines();

#%%
if(__name__ == "__main__"):
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
    draw_hotel_price(input_hotel_down, input_hotel_up, input_des)
    draw_weather(input_time_down, input_time_up, input_des)

#%%
    