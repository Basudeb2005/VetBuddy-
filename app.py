import streamlit as st
from PIL import Image

# Load VetBuddy logo
logo = Image.open("vetbuddy_logo.png")

# Set the page configuration
st.set_page_config(page_title="VetBuddy: Smarter Pet Care", page_icon=logo, layout="centered")

# Function to show the login page
def show_login_page():
    # Center the content manually using Streamlit's layout options
    st.markdown("<h1 style='text-align: center;'>🐾 Welcome to VetBuddy! 🐾</h1>", unsafe_allow_html=True)

    # Create columns to center the image
    left_co, cent_co, right_co = st.columns(3)
    with cent_co:
        st.image(logo, use_column_width=True)  # Centered logo using columns

    st.markdown("<h3 style='text-align: center;'>Smarter AI 💡, Healthier Pets 🐾, Happier Vets 😊</h3>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center;'>🔑 Login to Continue</h4>", unsafe_allow_html=True)

    # Input fields for login
    email = st.text_input("📧 Email Address", key="email")
    password = st.text_input("🔒 Password", type="password", key="password")

    # Cool login button with an emoji
    if st.button("🚀 Login"):
        if email and password:  # Simple validation
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Please enter both email and password.")

# Main application logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    st.empty()  # Clear the current content
    from pages.page1 import show_page1
    show_page1()
else:
    show_login_page()
