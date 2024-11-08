import streamlit as st
import pandas as pd
import numpy as np
import requests
import openpyxl
from io import StringIO


# def load_original_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return pd.read_csv(StringIO(response.text))
#     else:
#         st.error("Failed to load data from GitHub.")
#         return None

#################################################### Original Data ####################################################

## % of U.S. adults who say they ever use ... by ...
# us_usage_by_group_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/Social%20Media%20Usage_pivoted.xlsx"
# # us_usage_by_group = pd.read_excel("../data/original/Social Media Usage_pivoted.xlsx", header=0)
# response1 = requests.get(us_usage_by_group_url)
# if response1.status_code == 200:
#     us_usage_by_group = pd.read_excel(StringIO(response1.text), header=0)
# else:
#     st.error("Failed to load data from GitHub.")
# us_usage_by_group = load_original_data(us_usage_by_group_url)


## % of U.S. adults who say they ever use … (Polls from 2012-2021)
us_popular_platforms_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/which_social_media_platforms_are_most_popular_data_2024-01-31.csv"
response2 = requests.get(us_popular_platforms_url)
if response2.status_code == 200:
    us_popular_platforms = pd.read_csv(StringIO(response2.text), skiprows=3, delimiter=',', header=0)
else:
    st.error("Failed to load data from GitHub.")
# us_popular_platforms = pd.read_csv("../data/original/which_social_media_platforms_are_most_popular_data_2024-01-31.csv", 
#                                    skiprows=3, delimiter=',', header=0)
us_popular_platforms = us_popular_platforms.iloc[:-3, :]

us_popular_platforms.rename(columns={'\t\t\tYear': 'Year'}, inplace=True)
us_popular_platforms['Year'] = us_popular_platforms['Year'].str.replace('\t\t', '')
us_popular_platforms['Year'] = pd.to_datetime(us_popular_platforms['Year'])





#################################################### Streamlit ####################################################
st.title("American's Social Media Usage Dashboard 🇺🇸")
link1 = "https://www.pewresearch.org/internet/2024/01/31/americans-social-media-use/"
st.write("You can find the related report [here](%s)"%link1)
st.header("Original Data")
ori_on = st.toggle("Would you like to see the original data?", False)
# col1, col2 = st.columns(2, gap="medium", vertical_alignment="bottom")

def placeholder(lines):
    for _ in range(lines):
        st.markdown("\n")

if ori_on:
    
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        dim_option = st.selectbox("Please select a dimension you want to check",
                                    ('None', 'Age', 'Gender', 'Income', 'Political Affiliation', 'Race & Ethnicity'))
        # if dim_option == 'None':
        #     st.markdown(f"% of U.S. adults who say they ever use ... by ...")
        #     st.dataframe(us_usage_by_group)
        # else:
        #     st.markdown(f"% of U.S. adults who say they ever use ... by {dim_option}")
        #     st.dataframe(us_usage_by_group[us_usage_by_group['Dimension'] == dim_option])

    with col2:
        placeholder(5)
        st.markdown(f"% of U.S. adults who say they ever use ...(Polls from 2012-2021)")
        st.write(us_popular_platforms)


st.header("Reproduction 📊")



