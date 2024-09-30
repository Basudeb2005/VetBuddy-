import streamlit as st

# Initialize prescriptions list in session state if it doesn't exist
def init_session_state():
    if "prescriptions" not in st.session_state:
        st.session_state["prescriptions"] = []

# Add prescription entry and store in session state
def add_prescription():
    # Initialize session state if not already initialized
    init_session_state()

    # Species and breed information
    st.markdown("### Species and Breed")
    species = st.selectbox("Select the species", ["Dog", "Cat"])

    dog_breeds = ["Labrador Retriever", "German Shepherd", "Golden Retriever", "Bulldog", "Poodle", "Others"]
    cat_breeds = ["Persian", "Siamese", "Maine Coon", "Ragdoll", "Sphynx", "Others"]

    if species == "Dog":
        breed = st.selectbox("Select the breed", dog_breeds)
    else:
        breed = st.selectbox("Select the breed", cat_breeds)

    if breed == "Others":
        breed = st.text_input("Enter breed name")

    st.markdown("### Quick Entry")
    quick_entry = st.text_input(
        "Enter prescription details separated by semicolons (;): "
        "Medicine Name; Combination/Dosage; Times per Day; Number of Days; Before/After Meal; Additional Notes"
    )

    if st.button("Add from Quick Entry"):
        prescription = parse_prescription(f"{species};{breed};{quick_entry}")
        if prescription:
            st.session_state["prescriptions"].append(prescription)
            st.rerun()

    # Detailed entry for prescriptions
    st.markdown("### Detailed Entry")
    medicine_name = st.text_input("Medicine Name")
    combination = st.text_input("Combination/Dosage")
    times_per_day = st.number_input("Times per Day", min_value=1, max_value=10, step=1)
    num_days = st.number_input("Number of Days", min_value=1, max_value=365, step=1)
    meal_time = st.selectbox("When to Take", ["Before Meal", "After Meal"])
    additional_notes = st.text_area("Additional Notes")

    if st.button("Add Prescription"):
        prescription = {
            "species": species,
            "breed": breed,
            "medicine_name": medicine_name,
            "combination": combination,
            "times_per_day": times_per_day,
            "num_days": num_days,
            "meal_time": meal_time,
            "additional_notes": additional_notes
        }
        st.session_state["prescriptions"].append(prescription)
        st.rerun()

# Parse prescription from quick entry
def parse_prescription(quick_entry):
    try:
        parts = quick_entry.split(';')
        return {
            "medicine_name": parts[0].strip(),
            "combination": parts[1].strip(),
            "times_per_day": int(parts[2].strip()),
            "num_days": int(parts[3].strip()),
            "meal_time": parts[4].strip(),
            "additional_notes": parts[5].strip(),
        }
    except (IndexError, ValueError):
        st.error("Error: Please ensure all fields are filled correctly in the Quick Entry format.")
        return None

# Display prescriptions
def display_prescriptions():
    st.markdown("<h3 style='text-align: center;'>💊 Current Prescriptions</h3>", unsafe_allow_html=True)

    if st.session_state.get("prescriptions"):
        cols = st.columns([1, 1, 2, 2, 1, 1, 2, 2, 1])
        cols[0].markdown("**Species**")
        cols[1].markdown("**Breed**")
        cols[2].markdown("**💊 Medicine Name**")
        cols[3].markdown("**🧪 Combination/Dosage**")
        cols[4].markdown("**🕒 Times per Day**")
        cols[5].markdown("**📅 Number of Days**")
        cols[6].markdown("**🍽 When to Take**")
        cols[7].markdown("**📝 Additional Notes**")
        cols[8].markdown("**❌ Action**")

        for idx, prescription in enumerate(st.session_state["prescriptions"]):
            cols = st.columns([1, 1, 2, 2, 1, 1, 2, 2, 1])
            cols[0].write(prescription.get('species', ""))
            cols[1].write(prescription.get('breed', ""))
            cols[2].write(prescription['medicine_name'])
            cols[3].write(prescription['combination'])
            cols[4].write(prescription['times_per_day'])
            cols[5].write(prescription['num_days'])
            cols[6].write(prescription['meal_time'])
            cols[7].write(prescription['additional_notes'])
            if cols[8].button("❌", key=f"remove_{idx}_{prescription['medicine_name']}"):
                st.session_state["prescriptions"].pop(idx)
                st.rerun()

# Main function for the app
def show_page1():
    st.title("VetBuddy Prescription Page")

    # Prescription entry section
    st.markdown("<h3>Add a Prescription</h3>", unsafe_allow_html=True)
    add_prescription()

    # Display existing prescriptions
    st.markdown("<hr>", unsafe_allow_html=True)
    display_prescriptions()

if __name__ == "__main__":
    show_page1()
