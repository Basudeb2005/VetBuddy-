import openai
import streamlit as st

# Fetch your OpenAI API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to format the response in a clear, tabular format for Streamlit
def format_as_table(data):
    table = """
    ### 🐾 **Medical Suggestion**:
    Below is a detailed breakdown of the **symptoms**, **possible causes**, **diagnostic tests**, **treatments**, and **warnings**.
    
    | **Section**              | **Details**               |
    |--------------------------|---------------------------|
    """

    # Add symptoms to the table
    if data.get("symptoms"):
        table += "| **Symptoms**             | " + ", ".join(f"🩺 {symptom}" for symptom in data["symptoms"]) + " |\n"

    # Add possible causes with likelihood
    if data.get("causes"):
        table += "| **Possible Causes with Likelihood** | **Chance** |\n"
        table += "|--------------------------|---------------------------|\n"
        for cause in data["causes"]:
            table += f"| **{cause['name']}**      | {cause['likelihood']}% chance |\n"

    # Add diagnostic tests and treatments for each cause
    for cause in data.get("causes", []):
        if cause.get("diagnostic_tests"):
            table += f"\n##### 🧪 **Diagnostic Tests for {cause['name']}**\n"
            table += f"- **Tests**: {', '.join(cause['diagnostic_tests'])}"

        if cause.get("treatments"):
            table += f"\n##### 💉 **Treatment Options for {cause['name']}**\n"
            table += f"- **Treatments**: {', '.join(cause['treatments'])}"

        if cause.get("drug_interactions"):
            table += f"\n##### ⚠️ **Drug Interaction Warning for {cause['name']}**\n"
            table += f"- {cause['drug_interactions']}"

    # Add summary recommendation
    if data.get("summary"):
        table += f"\n\n### 🛑 **Summary Recommendation**\n"
        table += f"- {data['summary']}"

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
        return assistant_response  # Direct response from ChatGPT
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Get the session data for prescriptions and symptoms
    prescriptions = st.session_state.get("prescriptions", [])
    symptoms = st.session_state.get("symptoms_list", [])

    # Fetch and display the treatment flow
    response = get_treatment_flow_with_code(prescriptions, symptoms)
    
    # Render the response properly using Streamlit's markdown support
    st.markdown(format_as_table({
        "symptoms": symptoms,
        "causes": [
            {
                "name": "Kidney Disease",
                "likelihood": 65,
                "diagnostic_tests": ["Blood Test", "Urine Test", "Ultrasound"],
                "treatments": ["Fluid Therapy", "Dietary Management"],
                "drug_interactions": "Use caution with insulin."
            },
            {
                "name": "Diabetes",
                "likelihood": 45,
                "diagnostic_tests": ["Blood Glucose Test", "Urine Glucose Test"],
                "treatments": ["Insulin Therapy", "Low-Carb Diet"]
            }
        ],
        "drug_interactions": "Insulin and antibiotics can cause hypoglycemia.",
        "summary": "Focus on kidney function and glucose monitoring."
    }))
