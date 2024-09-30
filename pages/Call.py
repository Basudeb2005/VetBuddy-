import openai
import streamlit as st



# Load environment variables (for secret management)


# Fetch your OpenAI API key from environment variables
openai.api_key = st.secrets["OPENAI_API_KEY"]
# Function to format the response in a clear tabular format
def format_as_table(data):
    table = """
    ### 🐾 Medical Suggestion:
    Below is a detailed breakdown of the symptoms, possible causes, diagnostic tests, treatments, and warnings.
    
    | **Section**              | **Details**               |
    |--------------------------|---------------------------|
    """

    # Add symptoms to the table
    if data.get("symptoms"):
        table += "| **Symptoms**             | " + ", ".join(f"🩺 {symptom}" for symptom in data["symptoms"]) + " |\n"

    # Add possible causes with likelihood
    if data.get("causes"):
        for cause in data["causes"]:
            table += f"| **{cause['name']}**      | {cause['likelihood']}% chance |\n"

    # Add diagnostic tests and treatments for each cause
    for cause in data.get("causes", []):
        table += f"| **{cause['name']}** Diagnostic Tests:\n"
        if cause.get("diagnostic_tests"):
            table += "| **🧪 Diagnostic Tests**      | " + ", ".join(f"🔍 {test}" for test in cause["diagnostic_tests"]) + " |\n"
        if cause.get("treatments"):
            table += "| **💊 Treatment Options**     | " + ", ".join(f"💉 {treatment}" for treatment in cause["treatments"]) + " |\n"
        if cause.get("drug_interactions"):
            table += "| **⚠️ Drug Interaction Warning** | " + cause["drug_interactions"] + " |\n"

    # Add summary recommendation
    if data.get("summary"):
        table += "| **🛑 Summary Recommendation** | " + data["summary"] + " |\n"

    return table

# Function to fetch response from ChatGPT
def get_treatment_flow_with_code(prescriptions, symptoms):
    # Extract prescription details
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
        
        # Get the response from ChatGPT
        assistant_response = response.choices[0].message.content
        
        # Assuming ChatGPT returns a structured output, we would process it into the table
        # Here, we assume the ChatGPT response is already structured as required.
        return assistant_response  # Direct response from ChatGPT
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Get the session data for prescriptions and symptoms
    prescriptions = st.session_state.get("prescriptions", [])
    symptoms = st.session_state.get("symptoms_list", [])

    # Fetch and display the treatment flow
    response = get_treatment_flow_with_code(prescriptions, symptoms)
    st.markdown(response)  # Display the response in a table format
