import streamlit as st


st.title("Match Results")
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
image_url = "https://vedsubrandwebsite.s3.amazonaws.com/miscellaneous/DALL%C2%B7E+2024-09-17+12.16.40+-+A+night+scene+of+a+cricket+stadium+under+floodlights%2C+featuring+a+cricket+pitch+at+the+center.+The+stadium+is+set+for+a+major+event%2C+with+bright+flood.webp"

    # Display the image
st.image(image_url, caption="Power Play", use_column_width=True)