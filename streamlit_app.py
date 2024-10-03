import streamlit as st
import pymongo
import time


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
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
collection_admin = db_powerplay["admin"]

def login():
    ADMIN_ACCESS_KEY = st.secrets.ADMIN_ACCESS_KEY
    ADMIN_SECRET_KEY = st.secrets.ADMIN_SECRET_KEY
    with st.form("Team Details",clear_on_submit=True):
        
        st.subheader("Admin Login")
        user = st.text_input("Username :")
        password = st.text_input("Password :", type="password")
        login_button = st.form_submit_button(label = "Login")

        if login_button:
            try:
                # credentials = collection_admin.find_one({"Username":user, "Password": password})

                if user == ADMIN_ACCESS_KEY and password == ADMIN_SECRET_KEY:
                    st.session_state.logged_in = True
                    st.success("Login Successful")
                    # time.sleep(3)
                    st.rerun()
                    #  home.main()
                else: 
                     st.error("Invalid Credentials")
            except Exception as e:
                 st.error(f"Error: {str(e)}")

def logout():
        st.success("Logout Successful!")
        # st.warning("Login to access admin panel!")
        st.session_state.logged_in = False
        st.session_state.clear()
        st.info("Redirecting to access panel home! please wait....")
        # time.sleep(1)
        # if st.button("Click to access login panel"):
        st.rerun()
            # login()
             
        


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

search = st.Page("info/fixture.py", title="Fixtures", icon="📆",  default=True)
history = st.Page("info/match.py", title="History", icon="🏏")
sponsors = st.Page("info/sponsers.py", title = "Sponsors", icon = "💸" )
createfixture = st.Page("admin/createfixture.py", title =" Create Fixtures", icon="⏳" )
team = st.Page("admin/registration.py", title="Team Registration", icon="🧑‍🤝‍🧑")
player = st.Page("admin/players.py", title="Player Registration", icon="❗")
donors = st.Page("admin/donors.py", title = "Sponsors Registration", icon = ":material/money:")
score = st.Page("admin/scoring.py", title= "Score Card", icon="📝")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Admin": [team, player, donors, createfixture,score],
            "Panel": [search,history,sponsors ],
            # [dashboard, bugs, alerts],
        }
    )
    
else:
    pg = st.navigation( {"Account":[login_page],
                       "Panel": [search, history, sponsors],})

pg.run()
