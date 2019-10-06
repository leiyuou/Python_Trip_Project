import pandas as pd
import os
os.chdir("/Users/shanyue/Github/Python_Trip_Project")
import folium

# San Francisco latitude and longitude values
latitude = 37.77
longitude = -122.42

# Create map and display it
san_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Display the map of San Francisco
san_map.save("map/map.html")
