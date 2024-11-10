import streamlit as st


pages = {
    "Overview 👀": [
        st.Page("app_pages/00_Welcome🎈.py", title="DSS5201 About the Project")
    ],
    "Contents 📚": [
        st.Page("app_pages/01_Social_Media_Usage_in_US📱.py", title="US Social Media Usage 📱"),
        st.Page("app_pages/02_Supplement🔍.py", title="Supplementary Research 🔍")
    ]
}
pg = st.navigation(pages)
pg.run()