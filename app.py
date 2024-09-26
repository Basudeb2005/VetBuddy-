import streamlit as st
from PIL import Image
from pages.page1 import show_page1  # Import the function from page1.py

# Load VetBuddy logo
logo = Image.open("vetbuddy_logo.png")

# Set the page configuration
st.set_page_config(page_title="VetBuddy: Smarter Pet Care", page_icon=logo, layout="centered")

# Function to show the login page
def show_login_page():
    st.markdown(
        """
        <style>
        .right-align {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            margin-left: 15%;  /* Shift content 15% to the right */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="right-align">', unsafe_allow_html=True)
    st.image(logo)  # Display the logo shifted to the right
    st.title("Welcome to VetBuddy")

    if st.button("Login"):
        st.session_state['logged_in'] = True  # Set a session state flag
        st.experimental_rerun()  # Rerun the script to apply the change

    st.markdown("</div>", unsafe_allow_html=True)

# Main application logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    show_page1()  # Call the function from page1.py
else:
    show_login_page()