import streamlit as st

def parse_prescription(prescription_text):
    try:
        parts = [part.strip() for part in prescription_text.split(';')]
        if len(parts) == 6:
            return {
                "medicine_name": parts[0],
                "combination": parts[1],
                "times_per_day": int(parts[2]),
                "num_days": int(parts[3]),
                "meal_time": parts[4],
                "additional_notes": parts[5]
            }
    except Exception as e:
        st.error(f"Error parsing prescription: {e}")
    return None

def add_prescription():
    if "prescriptions" not in st.session_state:
        st.session_state["prescriptions"] = []

    st.markdown("### Quick Entry")
    quick_entry = st.text_input(
        "Enter prescription details separated by semicolons (;): "
        "Medicine Name; Combination/Dosage; Times per Day; Number of Days; Before/After Meal; Additional Notes"
    )
    
    if st.button("Add from Quick Entry"):
        prescription = parse_prescription(quick_entry)
        if prescription:
            st.session_state["prescriptions"].append(prescription)
            st.experimental_rerun()

    st.markdown("### Detailed Entry")
    medicine_name = st.text_input("Medicine Name")
    combination = st.text_input("Combination/Dosage")
    times_per_day = st.number_input("Times per Day", min_value=1, max_value=10, step=1)
    num_days = st.number_input("Number of Days", min_value=1, max_value=365, step=1)
    meal_time = st.selectbox("When to Take", ["Before Meal", "After Meal"])
    additional_notes = st.text_area("Additional Notes")

    if st.button("Add Prescription"):
        st.session_state["prescriptions"].append({
            "medicine_name": medicine_name,
            "combination": combination,
            "times_per_day": times_per_day,
            "num_days": num_days,
            "meal_time": meal_time,
            "additional_notes": additional_notes
        })
        st.experimental_rerun()

def display_prescriptions():
    st.markdown("<h3 style='text-align: center;'>💊 Current Prescriptions</h3>", unsafe_allow_html=True)

    if st.session_state.get("prescriptions"):
        # Create the table headers
        cols = st.columns([2, 2, 1, 1, 2, 2, 1])
        cols[0].markdown("**💊 Medicine Name**")
        cols[1].markdown("**🧪 Combination/Dosage**")
        cols[2].markdown("**🕒 Times per Day**")
        cols[3].markdown("**📅 Number of Days**")
        cols[4].markdown("**🍽 When to Take**")
        cols[5].markdown("**📝 Additional Notes**")
        cols[6].markdown("**❌ Action**")

        # Fill the table rows with prescription data
        for idx, prescription in enumerate(st.session_state["prescriptions"]):
            cols = st.columns([2, 2, 1, 1, 2, 2, 1])
            cols[0].write(prescription['medicine_name'])
            cols[1].write(prescription['combination'])
            cols[2].write(prescription['times_per_day'])
            cols[3].write(prescription['num_days'])
            cols[4].write(prescription['meal_time'])
            cols[5].write(prescription['additional_notes'])
            if cols[6].button("❌", key=f"remove_{idx}_{prescription['medicine_name']}"):
                st.session_state["prescriptions"].pop(idx)
                st.experimental_rerun()

