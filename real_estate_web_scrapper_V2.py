# Create data pipeline for real estate in Mauritius useing BeautifulSoup and Pandas

#   Import libraries
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#   Initialise global variables 
titles = []
locations = []
prices = []
features = []
source = [] 

#   Set up the range through which the web pages will be explored
pages = np.arange(1, 650, 50)

#   Create a coordinates Pandas DataFrame to associate each city with their respective lat, lng
coordinates = pd.read_csv('mu_city_coordinates.csv')

# Function to scrape L'Express Property and return a Pandas DataFrame realestate_db
for page in pages:

    page = requests.get("https://www.lexpressproperty.com/en/buy-mauritius/all/?currency=MUR&filters[interior_unit][eq]=m2&filters[land_unit][eq]=m2&p=" + str(page))

    soup = BeautifulSoup(page.content, "html.parser")

    lists = soup.find_all('div', class_ = "card-result-gallery")
    
    lists1 = soup.find_all('div', class_ = "ResultCardItem")

    # Loop through each container
    for list in lists:

            #title
            title = list.find('a', class_ = "").text
            titles.append(title) 
                        
            #location
            location = list.find('address').text
            locations.append(location)

            # price
            price = list.find('strong', class_ = "price").text
            prices.append(price)

            #features
            feature = list.find('ul', class_ = "option-list").text
            features.append(feature)

realestate_db = pd.DataFrame({
'title': titles,
'location': locations,
'price': prices,
'features': features,
})

try:
  realestate_db[["pro_type", "bedroom","surface_area"]] = realestate_db.title.apply(lambda x: pd.Series(str(x).split("-")))
except:
  realestate_db[["pro_type", "bedroom","surface_area", "misc"]] = realestate_db.title.apply(lambda x: pd.Series(str(x).split("-")))
else:
  print("Columns must be same length as key. Check first split")
# realestate_db[["pro_type", "bedroom","surface_area"]] = realestate_db.title.apply(lambda x: pd.Series(str(x).split("-")))
realestate_db[['type_1', 'type_2']] = realestate_db.pro_type.apply(lambda x: pd.Series(str(x).split("/"))) 
realestate_db[['region', 'sector']] = realestate_db.location.apply(lambda x: pd.Series(str(x).split(",")))
realestate_db.price = realestate_db.price.str.replace(',', '')
realestate_db.price = realestate_db.price.str.replace('Rs', '')
realestate_db[['num_bedroom','bed']] = realestate_db['bedroom'].loc[realestate_db['bedroom'].str.split().str.len() == 2].str.split(expand=True)
realestate_db[['empty_space', 'area', 'unit']] = realestate_db.surface_area.apply(lambda x: pd.Series(str(x).split(" ")))
realestate_db.bed = realestate_db.bed.str.replace('m²', '')

#   Merge realestate_db and coordinates database to obtain the corresponding coordinates of each city in realestate_db
realestate_db = realestate_db.merge(coordinates, how='inner', on=None, left_on='region', right_on='city', sort=False, copy=False)

# print(realestate_db)

# build an interactive map using Streamlit Maps

import streamlit as st

# App title
st.title ("Real Estates in Mauritius")

# Header for map element 
st.markdown("Property location Map")

# Map app 
df = pd.DataFrame(realestate_db, columns=['lat', 'lon'])
st.map(df)

# Map caption 
st.caption('Properties on sale with generalised location')

# Bar Chart of Price Range in Mauritius - Use plotly 

# import plotly.figure_factory as ff
import plotly.express as px
# import plotly.plotly as py
import plotly.graph_objects as go
# from plotly.tools import FigureFactory as FF
import chart_studio.plotly as py


#   Bar chart with Plotly Express
bar_chart = px.bar(
    realestate_db,
    x='location', y='price',
    title="location v/s prices",
    color="price")

# Plot!
# bar_chart.show()

#   Box plot of Real Estate Price in Mauritius per region
boxplot_price_per_region = px.box(realestate_db, x="sector", y="price", points="all")

boxplot_sfc_area_region = px.box(realestate_db, x="area", y="price")

boxplot_price_per_region.update_traces(quartilemethod="inclusive")

# boxplot_price_per_region.show()

# boxplot_sfc_area_region.show()

# Plot!
st.plotly_chart(bar_chart, use_container_width=True)
st.plotly_chart(boxplot_sfc_area_region, use_container_width=True)
st.plotly_chart(boxplot_price_per_region, use_container_width=True)


