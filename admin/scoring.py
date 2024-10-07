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
from bson.objectid import ObjectId

# Initialize a session state to store selected teams for fixtures
if 'match_id' not in st.session_state:
    st.session_state.match_id = None
if 'document_id' not in st.session_state:
    st.session_state.document_id = []
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'MoM' not in st.session_state:
    st.session_state.MoM = None
# if 'A_status' not in st.session_state:
#     st.session_state.A_status = None
# if 'B_status' not in st.session_state:
#     st.session_state.B_status = None
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'teamA' not in st.session_state:
    st.session_state.teamA = None
if 'teamB' not in st.session_state:
    st.session_state.teamB = None
if 'playerA' not in st.session_state:
    st.session_state.playerA = []
if 'playerB' not in st.session_state:
    st.session_state.playerB = []

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
        st.error(f"Connection failure: {str(e)}")

# Database Collections
client = init_connection()
db_powerplay = client["Powerplay"]
teams_collection = db_powerplay["registration"]
player_collection = db_powerplay["players"]
matches_collection = db_powerplay["matches"]

# Fetch matches from MongoDB
st.session_state.matches = list(matches_collection.find({"Winner":None},{"_id":0, "MatchID":1}))
# matches = matches_collection.distinct("MatchID")
match_list = ["Select"]
for match in st.session_state.matches:
    match_list.append(match.get("MatchID"))
    

if st.session_state.stage == 0:
 
    # st.write(st.session_state.match_id,st.session_state.winner,st.session_state.MoM, st.session_state.playerA)
    with st.container():
        st.session_state.match_id = st.selectbox("Select Match", match_list)
        if st.button("check"):
            try:
                teams = matches_collection.find_one({"MatchID": st.session_state.match_id}, {"_id": 0, "TeamA": 1, "TeamB": 1})
                st.session_state.teamA = teams.get("TeamA")
                st.session_state.teamB = teams.get("TeamB")
                # players = list(player_collection.find({"team":{"$in":[st.session_state.teamA, st.session_state.teamB]}},{"_id":0,"player":1, "aadhar":1}))
                playerA = list(player_collection.find({"team":st.session_state.teamA}, {"_id":0,"player":1, "aadhar":1}))
                playerB = list(player_collection.find({"team":st.session_state.teamB}, {"_id":0,"player":1, "aadhar":1}))
    
                for player in playerA:
                    player_id = str(player.get("player")) + "-" + str(player.get("aadhar"))
                    st.session_state.playerA.append(player_id)
                for player in playerB:
                    player_id = str(player.get("player")) + "-" + str(player.get("aadhar"))
                    st.session_state.playerB.append(player_id)
            except:
                st.success("all score card updated!")
            
            
    if st.session_state.match_id != "Select":
        with st.form("stage0", clear_on_submit=False):
                    st.session_state.winner = st.selectbox("Select Winner", options=["Select",st.session_state.teamA, st.session_state.teamB])
                    option_player = ["Select"] + st.session_state.playerA + st.session_state.playerB
                    
                    st.session_state.MoM = st.selectbox("Man of the Match", options=option_player)
                     
                    # st.session_state.MoM, st.session_state.MoMID = string.split("-")
            
                    if st.form_submit_button("update"): 
                        
                        # st.write(st.session_state.match_id,st.session_state.winner,st.session_state.MoM)
                        try:
                            matches_collection.update_one({"MatchID": st.session_state.match_id}, {"$set": {"Winner": st.session_state.winner,
                                                                                                           "MoM": st.session_state.MoM.split("-")[0],
                                                                                                           "MoMID": st.session_state.MoM.split("-")[1] }})
                            # matches_collection.update_one({"MatchID": st.session_state.match_id}, {"$set": {"MoM": st.session_state.MoM}})
                            
                            st.success("record updated successfully!")
                            st.session_state.stage = 1
                            st.session_state.playerA = []
                            st.session_state.playerB = []
                            st.rerun()
                    
                        except Exception as e:
                            st.error(f"Failed to update winner: {str(e)}")
                        
                        #query to update the collection



elif st.session_state.stage == 1:
    st.success(f"Winner:{st.session_state.winner}, MoM: {st.session_state.MoM}")
    colsa1, colsa2, colsa3, colsa4 = st.columns(4)
    with st.form("stage1teamA"):
        st.info(f"{st.session_state.teamA}")
        runA = st.number_input(label="Runs Scored (Team A):", min_value=0, step=1, key="teamArun")
        wicketA = st.number_input(label="Wickets Fallen (Team A):", min_value=0, max_value=9, step=1, key ="teamAwkt")
        
        st.markdown("____________________________")

        st.info(f"{st.session_state.teamB}")
        runB = st.number_input(label="Runs Scored (Team B):", min_value=0, step=1, key="teamBrun")
        wicketB = st.number_input(label="Wickets Fallen (Team B):", min_value=0, max_value=9, step=1, key ="teamBwkt")
        if st.form_submit_button(label= "update"):
            try:
                    matches_collection.update_one({"MatchID": st.session_state.match_id}, {"$set": {"TeamARun": runA, "TeamAWkt": wicketA,"TeamBRun": runB, "TeamBWkt": wicketB }})
                    st.success("Team data updated successfully!")
                    st.session_state.stage = 2
                    st.rerun()

            except Exception as e:
                    st.error(f"Update failed for Team A: {str(e)}")
            

elif st.session_state.stage == 2:

    playerA = list(player_collection.find({"team":st.session_state.teamA}, {"_id":1,"player":1, "aadhar":1, "photo":1}))
    player_count = 1
    submit_count = 0
    st.info(f"{st.session_state.teamA}")

    for player in playerA:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            image_url = player.get("photo")
            
            st.markdown(f"""
                <div style='text-align: center;'>
                    <img src="{image_url}" style="border-radius: 100%; width:80px; height:80px; margin-top:10px; box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px;">
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.text(f"{player_count}. {player.get("player")} {player.get("aadhar")}")
        with col3:
            runs = st.number_input("Runs:", min_value=0, step=1, key=f"{player.get('_id')}_run")
        with col4:
            wickets = st.number_input("Wickets:", min_value=0, max_value=9, step=1, key=f"{player.get('_id')}_wicket")
        with col5:
            catches = st.number_input("Catches:", min_value=0, max_value=9, step=1, key=f"{player.get('_id')}_catch")
        with col6:
            if player.get("_id") not in st.session_state.document_id:
                if st.button(label="Submit", key=f"{player.get('_id')}"):
                    # submit_count+=1
                    try:
                        document_id = ObjectId(player.get("_id"))
                        
                        player_collection.update_one(
                            {"_id": document_id},
                            {"$push": {
                                "score": {"$each": [runs]},
                                "wicket": {"$each": [wickets]},
                                "catch": {"$each": [catches]}
                            }}
                        )
                        st.success(f"Record updated for {player.get('player')}!")
                        st.session_state.document_id.append(player.get("_id"))
                        
                        # st.write(submit_count)
                        # time.sleep(2)
                        if player_count == len(playerA):
                            st.success(f"{st.session_state.teamA} players updated!")
                            st.session_state.stage = 3
                            st.rerun()
                        
                            
                    except Exception as e:
                        st.error(f"Failed to update player data: {str(e)}")
            else:
            
                st.success("updated!")
            player_count+=1
        st.markdown("__________________________________")
    

elif st.session_state.stage == 3:
    playerB = list(player_collection.find({"team":st.session_state.teamB}, {"_id":1,"player":1, "aadhar":1, "photo":1}))
    player_count = 1
    # submit_count = 1
    st.info(f"{st.session_state.teamB}")
    for player in playerB:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            image_url = str(player.get("photo"))
            
            st.markdown(f"""
                <div style='text-align: center;'>
                    <img src="{image_url}" style="border-radius: 100%; width:80px; height:80px; margin-top:10px; box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px;">
                </div>
            """, unsafe_allow_html=True)
            # st.text_area(image_url, key=f"{player.get('_id')}_img")
        with col2:
            st.text(f"{player_count}. {player.get("player")} {player.get("aadhar")}")
        with col3:
            runs = st.number_input("Runs:", min_value=0, step=1, key=f"{player.get('_id')}_run")
        with col4:
            wickets = st.number_input("Wickets:", min_value=0, max_value=9, step=1, key=f"{player.get('_id')}_wicket")
        with col5:
            catches = st.number_input("Catches:", min_value=0, max_value=9, step=1, key=f"{player.get('_id')}_catch")
        with col6:
            if player.get("_id") not in st.session_state.document_id:
                if st.button(label="Submit", key=f"{player.get('_id')}"):
                    try:
                        
                        document_id = ObjectId(player.get("_id"))
                        player_collection.update_one(
                            {"_id": document_id},
                            {"$push": {
                                "score": {"$each": [runs]},
                                "wicket": {"$each": [wickets]},
                                "catch": {"$each": [catches]}
                            }}
                        )
                        st.success(f"Record updated for {player.get('player')}!")
                        st.session_state.document_id.append(player.get("_id"))
                        
                        # submit_count+=1
                        # st.success(f"Record updated for {player.get('player')}!")
                        if player_count == len(playerB):
                            st.success(f"{st.session_state.teamB} players updated!")
                            
                        
                            st.session_state.matches = []

                            st.session_state.stage = 0

                            st.session_state.teamA = None

                            st.session_state.teamB = None

                            st.session_state.playerA = []

                            st.session_state.playerB = []

                            st.session_state.match_id = None

                            st.session_state.document_id = []

                            st.session_state.winner = None

                            st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update player data: {str(e)}")
            else:
            
                st.success("updated!")
            player_count+=1
        st.markdown("__________________________________")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   

