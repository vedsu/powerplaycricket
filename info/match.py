import streamlit as st

col1, col2 = st.columns(2)
with col1:
    st.page_link("https://powerplaycricket.in/", label="Home", icon="🏠")
with col2:
    st.subheader("Match Results")
    
# st.title("Match Results")
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
st.markdown(f"""
            <div style='text-align: center;'>
                <img src="{image_url}" style="border-radius: 50%; width:200px; height:200px; margin-top:10px; box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset;">
            </div>
        """, unsafe_allow_html=True)
    # Display the image
# st.image(image_url, caption="Power Play", use_column_width=True)
