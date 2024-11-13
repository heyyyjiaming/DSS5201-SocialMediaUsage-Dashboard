import streamlit as st
from PIL import Image
import requests
from io import BytesIO

github_url = "https://github.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard"
st.title("DSS5201 Data Visualization Group [Project](%s)"%github_url)
st.header("Welcome to our dashboard! 👾")
st.write(
    "In this dashboard, we will reproduce the graphs from web and explore the social media usage in the US."
)
# st.image("./img/cover.jpg")
cover_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/img/cover.jpg"
# response = requests.get(cover_url)
# if response.status_code == 200:
#     img = Image.open(BytesIO(response.content))
    
# st.image(img)
st.image(cover_url)

st.subheader("Group Members (in alphametic order):")
st.write("Ding Jiaming, Li Jingming, Niu Muyuan, Zhang Yi")