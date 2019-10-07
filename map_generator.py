#%%

############################################################
# This module is to generate map of the plan
############################################################ 

import pandas as pd
import os
os.chdir("/Users/shanyue/Github/Python_Trip_Project/")
import folium
import json
import numpy as np
import math

# latitude and longitude values
with open("dataset/AdelaideMetroStops_GDA2020.json",'r') as load_f:
    load_dict = json.load(load_f)

bus_latitudes = []
bus_longitudes = []
bus_labels = []

for line_dt in load_dict['features']:
    bus_labels.append(line_dt['properties']['stop_name'])
    bus_latitudes.append(line_dt['geometry']['coordinates'][1])
    bus_longitudes.append(line_dt['geometry']['coordinates'][0])



def cal_distance(position_1, position_2):
    return np.sqrt(np.sum(np.square(np.array(position_1) - np.array(position_2))))/180*math.pi*6300000

def set_bus(target_position):
    distance = cal_distance(target_position, 
                                [bus_latitudes[0],bus_longitudes[0]])
    bus_stop = 0
    for i in range(len(bus_latitudes)):
        temp = cal_distance(target_position, 
                                [bus_latitudes[i],bus_longitudes[i]])
        if(temp<distance):
            distance = temp
            bus_stop = i
    return distance, bus_stop

def get_plan_route(place_list):
    target_lat = []
    target_lng = []
    target_label = []
    final_distance = 0
    for place in place_list:
        target_label.append(place[0])
        target_lat.append(place[1])
        target_lng.append(place[2])
        distance, bus_stop = set_bus([place[1], place[2]])
        final_distance += distance
        target_label.append(bus_labels[bus_stop])
        target_lat.append(bus_latitudes[bus_stop])
        target_lng.append(bus_longitudes[bus_stop])
    
    city_map = folium.Map(location=[-34.921230, 138.599503], zoom_start=15)

    for lat, lng, label in zip(target_lat, target_lng, target_label):
        folium.Marker([lat, lng], popup=label).add_to(city_map)

    points = []
    for lat, lng in zip(target_lat, target_lng):
        points.append(tuple([lat, lng]))

    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(city_map)

    # Save the map
    city_map.save("map/map.html")
    return target_label, final_distance
    
#%%
if(__name__ == "__main__"):
    df = pd.read_excel("dataset/map_place_lat_long.xlsx")
    df = list(df.values)
    target_label, final_distance = get_plan_route(df)
    for spot in target_label:
        print(spot)