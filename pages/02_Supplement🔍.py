import streamlit as st
import pandas as pd
import numpy as np
import requests
import openpyxl
from io import StringIO, BytesIO
import plotly.express as px
from itertools import chain


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
    
    
    
    
st.header("Average Daily Time Spent on Social Media")

st.markdown("Still working on it...")
# st.dataframe(us_avg_time_2023)
# st.dataframe(us_avg_time_by_age)


def plot_avg_time_by_age(data, platform):
    fig_data = data.loc[:, ['Age', platform]]
    fig = px.bar(data, x='Age', y=platform,
                 title=f'Average time spent on {platform} in the US by age group').update_traces(marker=dict(color=platform_color_dict[platform]))
    return fig

colors = ['blue', 'pink', 'green', 'orange']
platform_color_dict = dict(zip(us_avg_time_by_age.columns[1:], colors))

selected_platform = st.selectbox("Please select a platform below", list(chain(['None'],us_avg_time_by_age.columns[1:])))   
if selected_platform=='None':
    fig = px.bar(us_avg_time_by_age_melted, x='Age', y='Time', color='Platform', facet_col='Platform', facet_col_wrap=0,
                 title=f'Average time spent on different platforms in the US by age group')
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = plot_avg_time_by_age(us_avg_time_by_age, selected_platform)
    st.plotly_chart(fig, use_container_width=True)


