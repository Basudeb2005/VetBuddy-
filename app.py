import streamlit as st
from PIL import Image

# Load VetBuddy logo
logo = Image.open("vetbuddy_logo.png")

# Set the page configuration
st.set_page_config(page_title="VetBuddy: Smarter Pet Care", page_icon=logo, layout="centered")

# Define a function to display the login page
def show_login_page():
    st.markdown(
        """
        <style>
        .right-align {
            display: flex;
            flex-direction: column;
            align-items: flex-start;  /* Aligns items to the start of the flex container */
            margin-left: 15%;  /* Moves content 15% to the right */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="right-align">', unsafe_allow_html=True)
    st.image(logo)  # Display the logo shifted to the right
    st.title("Welcome to VetBuddy")
    if st.button("Login"):
        st.session_state['logged_in'] = True
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Main application logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    # Redirect to `page1.py`
    st.markdown(
        """
        <meta http-equiv="refresh" content="0; url=./page1.py">
        """,
        unsafe_allow_html=True
    )
else:
    show_login_page()