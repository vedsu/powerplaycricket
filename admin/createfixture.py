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
from datetime import datetime, time
from PIL import Image

# Initialize a session state to store selected teams for fixtures
if 'selected_teams' not in st.session_state:
    st.session_state.selected_teams = []
if 'match_fixture' not in st.session_state:
    st.session_state.match_fixture = []

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
# Initialize a list to store match fixtures
# match_fixtures = []

# Fetch teams from MongoDB
all_teams = teams_collection.find({})
team_list = [team['TeamName'] for team in all_teams]  # Extracting team names
# st.write(team_list)

# Function to remove selected teams from available options
def get_available_teams(selected_teams):
    return [team for team in team_list if team not in selected_teams]


# Streamlit page title
st.title("Create Match Fixtures")

# Get available teams based on previously selected teams
available_teams = get_available_teams(st.session_state.selected_teams)

# Input fields for the fixture
date = st.date_input("Select Match Date", datetime.today().date())

time = st.time_input("Select Match Time", time(8, 00),step=1800)
slot = st.selectbox("Select Match Slot", ["1", "2", "3"])
# Convert date and time to string
date_str = date.strftime("%Y-%m-%d")  # Convert to string format YYYY-MM-DD
time_str = time.strftime("%H:%M")  # Convert time to string format HH:MM

# Display the converted strings
# st.write("Date as string:", date_str)
# st.write("Time as string:", time_str)
with st.container():
# Dropdowns for selecting teams
    if len(available_teams) >= 2:
        team_a = st.selectbox("Select Team A", available_teams, key="team_a")
        # available_teams_for_b = get_available_teams([team_a])
        
        team_b = st.selectbox("Select Team B", available_teams , key="team_b")
    else:
        st.error("Not enough teams available for selection.")

    col1, col2 = st.columns(2)
    with col1:
    # Add a button to confirm fixture creation
        if st.button("Create Fixture"):
            if team_a and team_b and team_a != team_b:
                count = len(st.session_state.match_fixture)+1
                st.session_state.match_fixture.append({
                    "Date": date_str,
                    "Time": time_str,
                    "Slot": slot,
                    "TeamA": team_a,
                    "TeamB": team_b,
                    "MatchID": count,
                    "TeamARun": None,
                    "TeamBRun": None,
                    "TeamAWkt": None,
                    "TeamBWkt": None,
                    "MoM": None,
                    "Winner":None

                })
                st.session_state.selected_teams.extend([team_a, team_b])  # Track selected teams
                st.success(f"Fixture Created: {team_a} vs {team_b} on {date} at {time} ({slot})")
            else:
                st.error("Please enter valid team names and ensure Team A is different from Team B.")
    with col2:
# Reset the selected teams when desired
        if st.button("Reset Selections"):
            st.session_state.selected_teams = []
            st.session_state.match_fixture = []
            st.success("Team selections have been reset.")
            st.rerun()
# Display the match fixtures as a table
if len(st.session_state.match_fixture)>0:
    df_fixtures = pd.DataFrame(st.session_state.match_fixture)
    st.sidebar.subheader("Match Fixtures")
    # st.sidebar.dataframe(df_fixtures)
    st.sidebar.dataframe(df_fixtures[["Date", "Time", "Slot", "TeamA", "TeamB"]])
    if len(st.session_state.match_fixture) == len(team_list)/2:
        if st.sidebar.button("Submit"):
            fixtures_list = df_fixtures.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
            try:
                matches_collection.insert_many(fixtures_list)
                st.sidebar.success("fixtures completed!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
