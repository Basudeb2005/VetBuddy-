import openai
import streamlit as st

# Fetch your OpenAI API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to display the response in a structured and readable format
def format_as_table(data):
    # Section: Medical Suggestion Heading
    st.markdown("### 🐾 **VetBuddy Medical Report**")
    st.markdown("Here’s a structured breakdown of the pet's **symptoms**, **possible causes**, **diagnostic tests**, **treatments**, and **warnings**.")

    # Section: Symptoms
    if data.get("symptoms"):
        st.markdown("#### 🩺 **Symptoms**")
        st.markdown(f"- {', '.join(f'🩺 {symptom}' for symptom in data['symptoms'])}")
    else:
        st.warning("⚠️ **No symptoms entered. Please provide symptoms to generate a treatment flow.**")
        return  # Stop the function here if no symptoms are provided

    # Section: Possible Causes
    if data.get("causes"):
        st.markdown("#### 🧠 **Possible Causes with Likelihood**")
        causes_table = []
        for cause in data["causes"]:
            causes_table.append([cause["name"], f"{cause['likelihood']}%", cause["severity"].capitalize()])
        st.table(causes_table)  # Clean, structured table without numbering
    
    # Section: Diagnostic Tests and Treatments
    for cause in data.get("causes", []):
        st.markdown(f"##### 🧪 **Diagnostic Tests for {cause['name']}**")
        st.markdown(f"- **Tests**: {', '.join(cause['diagnostic_tests'])}")

        st.markdown(f"##### 💉 **Treatment Options for {cause['name']}**")
        st.markdown(f"- **Treatments**: {', '.join(cause['treatments'])}")

    # Section: Drug Interaction Warning
    if data.get("drug_interactions"):
        st.markdown("#### ⚠️ **Drug Interaction Warning**")
        st.warning(data["drug_interactions"])

    # Section: Summary Recommendation
    if data.get("summary"):
        st.markdown("#### 🛑 **Summary Recommendation**")
        st.info(data["summary"])

# Main function to fetch response from ChatGPT and format it based on session state
def get_treatment_flow_with_code(prescriptions, symptoms):
    # Check if symptoms are empty
    if not symptoms:
        return st.warning("⚠️ **Please enter symptoms to generate a treatment flow.**")
    
    # Extract prescription details from session state
    prescription_details = []
    for prescription in prescriptions:
        details = f"{prescription.get('medicine_name', 'N/A')} - {prescription.get('combination', 'N/A')} - {prescription.get('times_per_day', 'N/A')} times per day"
        prescription_details.append(details)

    # Construct the prompt for ChatGPT
    prompt = f"""
    You are a veterinary assistant tasked with diagnosing and treating a pet based on the following symptoms and prescriptions.

    Provide the information in a clean, professional tabular format with emojis where relevant. The columns should include **Symptoms**, **Possible Causes with Likelihood** (use percentages), **Diagnostic Tests**, **Treatments**, **Drug Interaction Warning**, and **Summary Recommendations**.

    Symptoms: {', '.join(symptoms)}
    Prescriptions: {', '.join(prescription_details) if prescription_details else 'None'}

    Begin with symptoms and proceed step by step.
    """

    try:
        # Call ChatGPT API with the dynamically generated prompt
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract the response from ChatGPT and process it
        assistant_response = response.choices[0].message.content
        format_as_table({
            "symptoms": symptoms,  # Use symptoms from the session state
            "causes": response.choices[0].message.get('causes', []),
            "drug_interactions": response.choices[0].message.get('drug_interactions', ''),
            "summary": response.choices[0].message.get('summary', '')
        })
    
    except Exception as e:
        st.error(f"⚠️ Error generating treatment flow: {e}")

# Main Streamlit entry point
if __name__ == "__main__":
    # Dynamically get prescriptions and symptoms from session state
    prescriptions = st.session_state.get("prescriptions", [])
    symptoms = st.session_state.get("symptoms_list", [])

    # Fetch and display the treatment flow based on the current session state
    get_treatment_flow_with_code(prescriptions, symptoms)
