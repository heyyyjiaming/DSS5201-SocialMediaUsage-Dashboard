import streamlit as st
import pandas as pd
import numpy as np
import requests
import openpyxl
from io import StringIO, BytesIO
import plotly.express as px
from itertools import chain



## DJM add
# Read data from GitHub
## Average time spent per day on select social media platforms in the United States in June 2023 
us_avg_time_2023_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/us-users-daily-engagement-with-leading-social-media-platforms-2023.xlsx"
response1 = requests.get(us_avg_time_2023_url)
if response1.status_code == 200:
    us_avg_time_2023 = pd.read_excel(BytesIO(response1.content), engine='openpyxl',
                                      sheet_name='Data', skiprows=5, header=None)
else:
    st.error("Failed to load data from GitHub.")
us_avg_time_2023 = us_avg_time_2023.iloc[:, 1:]
us_avg_time_2023.columns = ['platform', 'avg_time']

   
## Average daily time spent with selected social networks among internet users in the United States as of September 2023, by age (in minutes)  
us_avg_time_by_age_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/daily-minutes-spent-on-social-networks-in-the-us-2023-by-age.xlsx"
# us_avg_time_by_age = pd.read_excel("../data/supplement/daily-minutes-spent-on-social-networks-in-the-us-2023-by-age.xlsx",
#                                    sheet_name='Data', skiprows=4, header=0)
response2 = requests.get(us_avg_time_by_age_url)
if response2.status_code == 200:
    us_avg_time_by_age = pd.read_excel(BytesIO(response2.content), engine='openpyxl',
                                      sheet_name='Data', skiprows=4, header=0)
else:
    st.error("Failed to load data from GitHub.")
us_avg_time_by_age = us_avg_time_by_age.iloc[:-1, 1:]
us_avg_time_by_age.rename(columns={'Unnamed: 1': 'Age'}, inplace=True)
us_avg_time_by_age.iloc[:, 1:] = us_avg_time_by_age.iloc[:, 1:] * 100

us_avg_time_by_age_melted = us_avg_time_by_age.melt(id_vars='Age', var_name='Platform', value_name='Time')


def plot_avg_time_by_age(data, platform):
    fig_data = data.loc[:, ['Age', platform]]
    fig = px.bar(data, x='Age', y=platform,
                 title=f'Average time spent on {platform} in the US by age group').update_traces(marker=dict(color=platform_color_dict[platform]))
    return fig

colors = ['blue', 'pink', 'green', 'orange']
platform_color_dict = dict(zip(us_avg_time_by_age.columns[1:], colors))




## ZY add
# leading countries data
leading_countries_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/x-twitter_-countries-with-the-largest-audience-2024.xlsx"
response3 = requests.get(leading_countries_url)
if response3.status_code == 200:
    leading_countries = pd.read_excel(BytesIO(response3.content), engine='openpyxl',
                                      sheet_name='Data', skiprows=4, usecols="B:C", 
                                      names=["Country", "Audience_Size"])
else:
    st.error("Failed to load data from GitHub.")
    

# World countries GeoJSON data
# World countries GeoJSON data
geojson_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/world_countries.geojson"
response_geojson = requests.get(geojson_url)
if response_geojson.status_code == 200:
    world_geojson = response_geojson.json()  # Use .json() directly
else:
    st.error("Failed to load GeoJSON data from GitHub.")



st.header("Other Findings in Social Media Usage 🔍")

st.markdown("#### 1. 2023 US Daily Time spent on Different Social Network")
selected_platform = st.selectbox("Please select a platform below", list(chain(['All'],us_avg_time_by_age.columns[1:])))   
if selected_platform=='All':
        fig = px.bar(us_avg_time_by_age_melted, x='Age', y='Time', color='Platform', facet_col='Platform', facet_col_wrap=0,
                    title=f'Average time spent on different platforms in the US by age group')
        st.plotly_chart(fig, use_container_width=True)
else:
        fig = plot_avg_time_by_age(us_avg_time_by_age, selected_platform)
        st.plotly_chart(fig, use_container_width=True)

    
st.markdown("#### 2. 2024 Wordlwide X (Twitter) Audience")
with st.spinner("Loading the graph... Please wait... 🙇🏻‍♀️"):
    fig = px.choropleth_mapbox(
        data_frame=leading_countries, 
        geojson=world_geojson, 
        locations="Country", 
        color="Audience_Size",
        featureidkey="properties.ADMIN",  # Match the geojson country name field
        mapbox_style="carto-positron",
        center={"lat": 0, "lon": 20},  # Center on the world
        zoom=1.5,
        # color_continuous_scale="Blue",
        title="Countries with the Largest Twitter Audience in 2024"
    )
    st.plotly_chart(fig, use_container_width=True)

# st.plotly_chart(fig, use_container_width=True)
    


## LJM add
## Statistics of U.S. frequently used social media activities in 2019 by platforms 
us_sm_activities_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/us-social-media-activities-2019-by-platform.xlsx"
# us_sm_activities = pd.read_excel("../data/supplement/us-social-media-activities-2019-by-platform.xlsx.xlsx",
#                                    sheet_name='Data', skiprows=4, header=0)
response3 = requests.get(us_sm_activities_url)
if response2.status_code == 200:
    us_sm_activities = pd.read_excel(BytesIO(response3.content), engine='openpyxl',
                                      sheet_name='Data', skiprows=4, header=0)
else:
    st.error("Failed to load data from GitHub.")
us_sm_activities = us_sm_activities.dropna(how = 'all', axis = 0).dropna(how = 'all', axis = 1)
us_sm_activities = us_sm_activities.iloc[:, :-1]
us_sm_activities = us_sm_activities.rename(columns = {"Unnamed: 1" : "Activities"})
us_sm_activities = us_sm_activities.melt(id_vars = "Activities", var_name = "Platform", value_name = "Percentage")

st.markdown("#### 3.  Statistic of U.S. Social Media Activities in 2019 by Platforms")

def create_us_sm_activities_plot(data):
    fig = px.bar(data, x = 'Activities', y = 'Percentage', color = 'Platform', 
                  barmode = "group", title = 'US Social Media Activities by Platform in 2019')
    
    fig.update_yaxes(range=[0, 100], ticksuffix="%")

    return fig

us_sm_activities_plot = create_us_sm_activities_plot(us_sm_activities)
st.plotly_chart(us_sm_activities_plot, use_container_width=True)
    



