import streamlit as st
import streamlit as st
import pymongo
import random
import io
import requests
from datetime import datetime, time
from PIL import Image
import pandas as pd
import graphviz
# Initialize a session state to store selected teams for fixtures


# Database Connections
@st.cache_resource

def init_connection():
    try:
        db_username = st.secrets.db_username
        db_password = st.secrets.db_password
        mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)
        client = pymongo.MongoClient(mongo_uri)
        return client
    
    except Exception as e:
    
        st.error(f"Connection failure:{str(e)}")

# Database Collections

client = init_connection()
db_powerplay = client["Powerplay"]
teams_collection = db_powerplay["registration"]
matches_collection = db_powerplay["matches"]
list_matches = list(matches_collection.find({},{"_id":0}))
df_matches = pd.DataFrame(list_matches)


col1, col2 = st.columns(2)
with col1:
    st.page_link("https://powerplaycricket.in/", label="Home", icon="🏠")
with col2:
    st.subheader("Tournament Results")
st.subheader("",divider=True)
if df_matches:           
    st.dataframe(df_matches)

# else:
    image_url = "https://vedsubrandwebsite.s3.amazonaws.com/miscellaneous/DALL%C2%B7E+2024-09-17+12.16.40+-+A+night+scene+of+a+cricket+stadium+under+floodlights%2C+featuring+a+cricket+pitch+at+the+center.+The+stadium+is+set+for+a+major+event%2C+with+bright+flood.webp"

    st.markdown(f"""
                <div style='text-align: center;'>
                    <img src="{image_url}" style="border-radius: 100%; width:200px; height:200px; margin-top:10px; box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px;">
                </div>
            """, unsafe_allow_html=True)
 
