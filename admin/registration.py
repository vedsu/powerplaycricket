import streamlit as st
import pandas as pd
import numpy as np
import time
import boto3
import pymongo
import random
import string
import io
import requests
from datetime import datetime
from PIL import Image
import uuid

@st.cache_resource
def s3_connection():
    try:
        AWS_ACCESS_KEY = st.secrets.AWS_ACCESS_KEY
        AWS_SECRET_KEY = st.secrets.AWS_SECRET_KEY 

        s3_client = boto3.client(
        service_name = "s3",
        region_name = 'us-east-1',
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY)
        
        return s3_client
    except Exception as e:
        st.error(f"Connection failure:{str(e)}")

s3_client = s3_connection()


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
collection_reg = db_powerplay["registration"]


    
# def main():
# st.write("----------------------------------")

# generating registration number
team_number = len(list(collection_reg.find({})))+ 1
# team_number = 1
# get the current date in the format ddmmyy
current_date = datetime.now().strftime('%d%m%y')

# generate three-letter alphabetic string
random_alpha = ''.join(random.choices(string.ascii_uppercase, k=3))
registration_number = f"{current_date}#{random_alpha}#{team_number}"


# Display the QR code in sidebar
image_url = "https://vedsubrandwebsite.s3.amazonaws.com/PowerPlayCricket/PowerPlayQR.jpeg"

response = requests.get(image_url)
img = Image.open(io.BytesIO(response.content))
st.sidebar.image(img, caption="QR Code for PowerPlay Cricket " + registration_number, use_column_width=True)

with st.form("Team Details",clear_on_submit=True):
    
    st.subheader("Registration Form")
    st.info(f"Registration No: {registration_number}")
    team_name = st.text_input("Team Name:")
    team_image = st.file_uploader("Logo")
    manager_name =  st.text_input("Manager Name")
    captain_name = st.text_input("Captain Name", )
    payment_mode = st.radio("Payment Mode", ["QR", "Cash"], horizontal= True)
    reg_amt_paid = st.number_input("Registration Amount Paid:", min_value=0, max_value=700)
    
    reg_amt_due = 700 - reg_amt_paid
    # st.info(f"Regsitration Amount Due:{reg_amt_due}")
    admin_remark = st.text_area("Payment Description")
    submitted = st.form_submit_button(label="Register")
    if submitted:
        errors = []
        if not team_name:
            errors.append("Team Name is required.")
        if not manager_name:
            errors.append("Manager Name is required.")
        if not captain_name:
            errors.append("Captain Name is required.")
        
        # Validate logo upload
        if not team_image:
            errors.append("Team Logo is required.")
        
        # If there are errors, display them
        if errors:
            for error in errors:
                st.error(error)
        else:
            filename = f"{uuid.uuid4()}"
            try:
                bucket_name = "vedsubrandwebsite"
                object_key = filename
                s3_url = f"https://{bucket_name}.s3.amazonaws.com/PowerPlayCricket/player/{object_key}.png"
                # st.session_state[f'player_{st.session_state.current_player}_photo'] = s3_url
                photo = s3_url
                s3_client.put_object(
                Body=team_image, 
                Bucket=bucket_name, 
                Key=f'PowerPlayCricket/player/{object_key}.png'
                )
    
            except Exception as e:
                s3_url = f"{str(e)}"
            team_data = {
            "RegNo": registration_number,
            "TeamName": team_name,
            "TeamLogo": s3_url,
            "ManagerName": manager_name,
            "CaptainName": captain_name,
            "PaymentMode": payment_mode,
            "RegAmtPaid": reg_amt_paid,
            "RegAmtDue": reg_amt_due,
            "AdminRemark": admin_remark
            }
    
            st.info(f"Regsitration Amount Due:{reg_amt_due}")
            try:
    
                collection_reg.insert_one(team_data)
    
                st.success("Registration Successful")
                time.sleep(5)
                st.rerun()
            except Exception as e:
                st.error(f"Registration Failed, {str(e)}")


    

