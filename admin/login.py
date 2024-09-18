import streamlit as st
import pymongo
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
import admin.home as home

# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False




# with st.form("Team Details",clear_on_submit=True):
        
#         st.subheader("Admin Login")
#         user = st.text_input("Username :")
#         password = st.text_input("Password :", type="password")
#         login = st.form_submit_button(label = "Login")

#         if login:
#             try:
#                 credentials = collection_admin.find({"username":user, "password": password})
#                 if credentials:
#                      st.session_state.logged_in = True
#                      st.success("Login Successful")
#                 else: 
#                      st.error("Invalid Credentials")
#             except Exception as e:
#                  st.error(f"Error: {str(e)}")
             