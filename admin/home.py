import streamlit as st
import numpy as np
import admin.registration as registration

# def main():
st.header("HomePage")
tabTeam, tabempty1,tabempty2,tabempty3, tabPlayer= st.tabs(["🗃 Teams Registration", " ", " ",  " ",  " 📈 Players Registration"])
data = np.random.randn(10, 1)
tabTeam.subheader("Team Registration")
registration.main()
tabempty1
tabempty2
tabempty3
tabPlayer.subheader("A tab with the data")
tabPlayer.write(data)