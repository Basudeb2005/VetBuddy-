import streamlit as st
from pages.prescription import add_prescription, display_prescriptions


def show_page1():
    st.markdown("<h1 style='text-align: center;'>VetBuddy Prescription and Treatment Page</h1>", unsafe_allow_html=True)

    # Prescription Entry Section
    add_prescription()

    # Display Prescriptions Section
    display_prescriptions()

    # Existing Sections (Symptoms, Suggestions, etc.)
    st.markdown("<h3 style='text-align: center;'>🩺 Symptoms</h3>", unsafe_allow_html=True)
    if 'symptoms_list' not in st.session_state:
        st.session_state['symptoms_list'] = []

    # Input for new symptom
    new_symptom = st.text_input("Add a symptom", placeholder="Enter a symptom and press enter")

    # Prevent adding duplicates and ensure the symptom is non-empty
    if new_symptom:
        new_symptom = new_symptom.strip()  # Strip whitespace
        if new_symptom and new_symptom.lower() not in (s.lower() for s in st.session_state['symptoms_list']):
            st.session_state['symptoms_list'].append(new_symptom)
            st.experimental_rerun()  # Refresh the page to show the updated list

    # Display symptoms with the ability to remove
    if st.session_state['symptoms_list']:
        for i, symptom in enumerate(st.session_state['symptoms_list']):
            cols = st.columns([9, 1])
            cols[0].markdown(f"✅ {symptom}")
            if cols[1].button("❌", key=f"remove_symptom_{i}"):
                st.session_state['symptoms_list'].pop(i)
                st.experimental_rerun()

    st.markdown("<h3 style='text-align: center;'>💡 Suggestions and Treatment Flows</h3>", unsafe_allow_html=True)
    treatment = st.text_area("Write suggestions or treatment flows here...", height=100)

    st.markdown("<h3 style='text-align: center;'>⚠️ Drug Interaction Warning</h3>", unsafe_allow_html=True)
    drug_interaction = st.checkbox("Simulate")
    if drug_interaction:
        st.warning("Warning: The prescribed drugs may have {low/moderate/severe} interactions that could cause adverse effects.")

    if st.button("Direct me to treatment flow"):
        st.info("You will be directed to the detailed treatment flow... (This is a placeholder for actual redirection logic)")

    if st.button("Save"):
        st.success("Prescription and treatment plan saved!")

if __name__ == "__main__":
    show_page1()
