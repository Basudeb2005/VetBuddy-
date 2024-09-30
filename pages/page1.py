import streamlit as st
from pages.Call import get_treatment_flow_with_code  # Import the necessary function
from pages.prescription import *

# Function to reset the session state (to clear the page)
def reset_session():
    for key in st.session_state.keys():
        del st.session_state[key]

# Main function to display the page
def show_page1():
    st.markdown("<h1 style='text-align: center;'>VetBuddy Prescription and Treatment</h1>", unsafe_allow_html=True)

    # Reset button to clear the page state
    if st.button("Reset Page"):
        reset_session()
        st.rerun()

    # Prescription Entry Section (assuming functions exist for these)
    add_prescription()  # This should handle adding a prescription
    display_prescriptions()  # This should display current prescriptions

    # Symptoms Entry Section
    st.markdown("<h3 style='text-align: center;'>🩺 Symptoms</h3>", unsafe_allow_html=True)
    if 'symptoms_list' not in st.session_state:
        st.session_state['symptoms_list'] = []

    new_symptom = st.text_input("Add a symptom", placeholder="Enter a symptom and press enter")

    # Add new symptom to session state
    if new_symptom:
        new_symptom = new_symptom.strip()
        if new_symptom and new_symptom.lower() not in (s.lower() for s in st.session_state['symptoms_list']):
            st.session_state['symptoms_list'].append(new_symptom)
            st.rerun()  # Refresh the page

    # Display symptoms
    if st.session_state['symptoms_list']:
        for i, symptom in enumerate(st.session_state['symptoms_list']):
            cols = st.columns([9, 1])
            cols[0].markdown(f"✅ {symptom}")
            if cols[1].button("❌", key=f"remove_symptom_{i}"):
                st.session_state['symptoms_list'].pop(i)
                st.rerun()

    # # Suggestions and Treatment Flow
    # st.markdown("<h3 style='text-align: center;'>💡 Suggestions and Treatment Flows</h3>", unsafe_allow_html=True)
    # treatment = st.text_area("Write suggestions or treatment flows here...", height=100)

    # st.markdown("<h3 style='text-align: center;'>⚠️ Drug Interaction Warning</h3>", unsafe_allow_html=True)
    # drug_interaction = st.checkbox("Simulate")
    # if drug_interaction:
    #     st.warning("Warning: The prescribed drugs may have {low/moderate/severe} interactions that could cause adverse effects.")

    # Button to fetch treatment flow
    if st.button("Direct me to treatment flow"):
        st.info("Fetching treatment flow...")

        # Get prescriptions and symptoms
        prescriptions = st.session_state.get("prescriptions", [])
        symptoms = st.session_state.get("symptoms_list", [])

        # Call the imported function from Call.py
        response = get_treatment_flow_with_code(prescriptions, symptoms)
        if response:
            st.markdown("""
            ### Medical Suggestion:
            Below is a detailed breakdown of the symptoms, possible causes, diagnostic tests, treatments, and warnings. The content is represented in a structured tabular format for clarity.
            """)
            st.markdown(response)  # Display the treatment flow response
        else:
            st.error("Error generating treatment flow.")

    if st.button("Save"):
        st.success("Prescription and treatment plan saved!")

if __name__ == "__main__":
    show_page1()
