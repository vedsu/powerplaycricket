import streamlit as st
import requests
import pandas as pd
import pymongo
import boto3
from PIL import Image
import numpy as np
import uuid
from io import BytesIO

if 'current_player' not in st.session_state:
        st.session_state.current_player = 0

if 'team' not in st.session_state:
        st.session_state.team  = None
if 'selected_team_count' not in st.session_state:
        st.session_state.selected_team_count = 15

if  'player_count' not in st.session_state:
        st.session_state.player_count = 0





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
collection_team = db_powerplay["players"]

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
# team_names = collection_reg.distinct("TeamName")
# team_names = sorted(team_names)
team_list = list(collection_team.find({}, {"team":1, "player":1, "_id":0}))
df = pd.DataFrame(team_list)
df2 = df['team'].value_counts().reset_index()
df2.columns = ['team', 'count']
team_names = df2[df2['count']<15]['team'].to_list()


col1, col2, col3 = st.columns(3)
with col1:
        st.subheader("Player Registration")
with col3:
        if st.button("Cancel"):
                st.session_state.team = None
                st.session_state.selected_team_count = 15
                st.session_state.player_count = 0
                st.rerun()

if st.session_state.player_count == 0:
    # Add "select" as the first option
    teams = ["Select"]+sorted(team_names)
    with st.container():
    # with st.form("init", clear_on_submit=False):
            
        st.session_state.team = st.selectbox("Select Team: ", options = teams, placeholder="Choose a team")
        if st.session_state.team != "Select":
                st.session_state.selected_team_count = df2[df2['team'] == st.session_state.team]['count'].values[0]
        
        # Get the total number of players
                st.session_state.player_count = st.number_input("Total players for team",value="min", max_value=15, min_value=st.session_state.selected_team_count, step=1)
                if st.button(label="regsiter"):
                    st.rerun()


if st.session_state.team != "Select" and st.session_state.player_count > st.session_state.selected_team_count:
    

    st.subheader(f"Register players for {st.session_state.team} ")

   

    # Loop through each player until the total number of players is reached
    if st.session_state.current_player < st.session_state.player_count:
        key = f"player{st.session_state.current_player}"
        st.info(f"Register Player {st.session_state.current_player + 1} / {st.session_state.player_count}")
       
        # Create the form for the current player
        with st.form(key, clear_on_submit=True):
            player = st.text_input("Name :")
            type = st.radio("Type : ", ["Bat", "Bowl", "AR"], horizontal=True)
            # Create the FingerReader instance in debug mode.
            
            img_file_buffer = st.camera_input("Take a picture",disabled=False)


            # if img_file_buffer is not None:
            #     # To read image file buffer as a PIL Image:
            #     img = Image.open(img_file_buffer)

            #     # To convert PIL Image to numpy array:
            #     img_array = np.array(img)

            #     # Check the type of img_array:
            #     # Should output: <class 'numpy.ndarray'>
            #     st.write(type(img_array))

            #     # Check the shape of img_array:
            #     # Should output shape: (height, width, channels)
            #     st.write(img_array.shape)
            
            submit_button = st.form_submit_button(label="Submit")
            
            if submit_button and player:
                # Save the player's details (this is where you can store them, e.g., in a list or database)
                
                
                # st.session_state[f'player_{st.session_state.current_player}_name'] = player
                # # st.write(st.session_state[f'player_{st.session_state.current_player}_name'])
                # st.session_state[f'player_{st.session_state.current_player}_type'] = type

                
                if img_file_buffer is not None:
                    filename = f"{uuid.uuid4()}"
                    # Convert the image to bytes
                    image = Image.open(img_file_buffer)
                    image_bytes = BytesIO()
                    image.save(image_bytes, format='PNG')
                    image_bytes.seek(0)
                    try:
                        bucket_name = "vedsubrandwebsite"
                        object_key = filename
                        s3_url = f"https://{bucket_name}.s3.amazonaws.com/PowerPlayCricket/player/{object_key}.png"
                        # st.session_state[f'player_{st.session_state.current_player}_photo'] = s3_url
                        photo = s3_url
                        s3_client.put_object(
                        Body=image_bytes, 
                        Bucket=bucket_name, 
                        Key=f'PowerPlayCricket/player/{object_key}.png'
                        )

                    except Exception as e:
                        s3_url = f"{str(e)}"
                        
                try:               
                    document = {"team":st.session_state.team , "player":player,
                                "type":type,
                                "photo":photo,
                                "score":[], "wicket":[], "catch":[] }
                    collection_team.insert_one(document)
                    # Increment the player index to move to the next player
                    st.session_state.current_player += 1
                    
                    # Provide feedback
                    st.success(f"Player {st.session_state.current_player} registered successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error registering player: {str(e)}")
                
    else:
        st.success("All players have been registered!")
        if st.button(label="register another team"):
            st.session_state.current_player = 0
            st.session_state.team  = "Select"
            st.session_state.player_count = 0
            st.rerun()

    # Example of how to display the registered players
    if st.session_state.current_player > 0:
        st.subheader(f"{st.session_state.team} Players")
        col1, col2 = st.columns(2)
        for i in range(st.session_state.current_player):
            with col1:
                st.write(f"Player {i+1} registered")
                st.write("\n")
                
    #         with col2:
    #             # Display the image from session_state
                
    #             image_url = st.session_state.get(f'player_{i}_photo', None)
    #             # st.write(image_url)
    #             if image_url:
    #                 st.image(image_url,  width=70)





    
