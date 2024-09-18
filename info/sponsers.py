import streamlit as st
import pymongo
import pandas as pd
# st.title("Sponsor Page")
st.header(":blue[Dear Sponsors] :grey[Welcome to PowerPlay!] 💯 ", divider=True)

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
collection = db_powerplay["donors"]

# Fetch donor data from MongoDB
donors = collection.find({}).sort({"RegAmtPaid":1})  # Retrieve all donors

# Process data and display it
donor_list = []
for donor in donors:
    donor_info = {
        # "_id": str(donor.get('_id', '')),
        # "RegNo": donor.get('RegNo', ''),
        "DonorName": donor.get('DonorName', ''),
        # "PaymentMode": donor.get('PaymentMode', ''),
        "RegAmtPaid": donor.get('RegAmtPaid', ''),
        "Photo": donor.get('photo', ''),
        "AdminRemark": donor.get('AdminRemark', '')
    }
    donor_list.append(donor_info)

# Convert list to DataFrame for display
df_donors = pd.DataFrame(donor_list)

# Display donor data in table format
# st.dataframe(df_donors)
# Display individual details for each donor
for donor in donor_list:
    col1, col3= st.columns([2,1])
    with col1:
        st.subheader(f"{donor['DonorName']}")
    # st.write(f"RegNo: {donor['RegNo']}")
    # st.write(f"Payment Mode: {donor['PaymentMode']}")
        st.write(f"Amount: {donor['RegAmtPaid']}")
        st.caption(f"Description: {donor['AdminRemark']}")
    
        
    with col3:
        st.markdown(f"""
            <div style='text-align: center;'>
                <img src="{donor['Photo']}" style="border-radius: 50%; width:120px; height:120px; margin-top:20px; box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset;">
            </div>
        """, unsafe_allow_html=True)
    st.markdown(f"""
            <div style='border-bottom:1px solid #ff9933; margin-top: 5px'>
                
            </div>
        """, unsafe_allow_html=True)
        
