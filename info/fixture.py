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
col1, col2 = st.colummns(2)
with col1:
    st.page_link("https://powerplaycricket.in/", label = "Home", icon = "🏠")
# st.title("Cricket Tournament Fixture")
with col2:
    st.subheader("Tournament Fixture")

# Function to get team logo by matching team name
def get_team_logo(team_name):
    team = teams_collection.find_one({"TeamName": team_name})
    return team["TeamLogo"] if team else None
# Function to get matches for the selected date
def get_matches_by_date(selected_date):
    return matches_collection.find({"Date": str(selected_date)})
# Streamlit interface
st.markdown("""
        <style>
        div.stButton > button {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """, unsafe_allow_html=True)
    # if st.button("click to Vybe!"):
    #         st.session_state.default = True
    #         st.rerun()
        
        # URL of the image

if len(df_matches) < 1:
    
    image_url = "https://vedsubrandwebsite.s3.amazonaws.com/miscellaneous/DALL%C2%B7E+2024-09-17+12.16.40+-+A+night+scene+of+a+cricket+stadium+under+floodlights%2C+featuring+a+cricket+pitch+at+the+center.+The+stadium+is+set+for+a+major+event%2C+with+bright+flood.webp"
        # Display the image
    st.image(image_url, caption="Power Play", use_column_width=True)
else:
    # image_url = "https://vedsubrandwebsite.s3.amazonaws.com/miscellaneous/DALL%C2%B7E+2024-09-18+12.21.28+-+A+night+cricket+scene+under+bright+floodlights+with+players+actively+playing+on+the+pitch.+The+stadium+is+filled+with+a+cheering+crowd%2C+adding+to+the+.webp"
    # st.image(image_url, caption="Power Play", use_column_width= 'auto',)
    # Date input for the user to select
    selected_date = st.date_input("Select Date to View Matches", datetime.today().date())
    # Fetch matches for the selected date
    matches = list(get_matches_by_date(selected_date))
    
    if matches:
    # Organize matches by slot (Morning, Afternoon, Evening, Night)
        morning_matches = [m for m in matches if m["Slot"] == "1"]
        afternoon_matches = [m for m in matches if m["Slot"] == "2"]
        evening_matches = [m for m in matches if m["Slot"] == "3"]
     # Create tabs for each slot
    tab1, tab2, tab3 = st.tabs(["1️⃣👉", "2️⃣👉", "3️⃣👈"])
     # Morning Slot
    with tab1:
        st.subheader("Slot 1 Matches")
        if morning_matches:
            col1, col2, col3 = st.columns(3)
            for match in morning_matches:

                team_a_logo = get_team_logo(match['TeamA'])
                team_b_logo = get_team_logo(match['TeamB'])
                with col1:
                    st.image(team_a_logo, width=100, caption=match['TeamA'])
                with col2:
                    st.write("\n")
                    # st.error("V/S")
                    st.info(f"**{match['TeamA']} vs {match['TeamB']}** at {match['Time']}")
                with col3:
                    st.image(team_b_logo, width=100, caption=match['TeamB'])
        else:
            st.write("No matches scheduled for Slot 1.")

    # Afternoon Slot
    with tab2:
        st.subheader("Slot 2 Matches")
        if afternoon_matches:
            col1, col2, col3 = st.columns(3)
            for match in afternoon_matches:
                team_a_logo = get_team_logo(match['TeamA'])
                team_b_logo = get_team_logo(match['TeamB'])
                with col1:
                    st.image(team_a_logo, width=100, caption=match['TeamA'])
                with col2:
                    st.write("\n")
                    st.info(f"**{match['TeamA']} vs {match['TeamB']}** at {match['Time']}")
                    # st.error("V/S")
                with col3:
                    st.image(team_b_logo, width=100, caption=match['TeamB'])
        else:
            st.write("No matches scheduled for Slot 2.")

    # Evening Slot
    with tab3:
        st.subheader("Slot 3 Matches")
        if evening_matches:
            col1, col2, col3 = st.columns(3)
            for match in evening_matches:
                team_a_logo = get_team_logo(match['TeamA'])
                team_b_logo = get_team_logo(match['TeamB'])
                with col1:
                    st.image(team_a_logo, width=100, caption=match['TeamA'])
                with col2:
                    st.write("\n")
                    st.info(f"**{match['TeamA']} vs {match['TeamB']}** at {match['Time']}")
                    # st.error("V/S")
                with col3:
                    st.image(team_b_logo, width=100, caption=match['TeamB'])
        else:
            st.write("No matches scheduled for Slot 3.")
    st.write("----------------------------------------")
    st.dataframe(df_matches)

# # Displaying the rounds
# for round_number, round_matches in enumerate(fixture, start=1):
#     st.header(f'Round {round_number}')
#     for match_number, match in enumerate(round_matches, start=1):
#         st.write(f'Match {match_number}: {match[0]} vs {match[1]}')

# # Final match
# st.header('Final')
# st.write(f'Final: {fixture[-1][0][0]} vs {fixture[-1][0][1]}')
