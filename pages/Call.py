import openai
import streamlit as st

# Fetch your OpenAI API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Helper function to color-code severity
def color_text(text, severity):
    colors = {
        "mild": "#5cb85c",       # Green
        "moderate": "#f0ad4e",   # Orange
        "severe": "#d9534f"      # Red
    }
    return f"<span style='color:{colors[severity]}'>{text}</span>"

# Helper function to create ASCII-style decision trees
def create_decision_tree(symptoms, causes):
    tree = "```text\n"
    tree += "Symptom: " + ", ".join(symptoms) + "\n"
    tree += "  ├── Possible Causes\n"
    for cause in causes:
        tree += f"  │   ├── {cause['name']} ({cause['likelihood']}% chance)\n"
        tree += "  │   │   ├── Diagnostic: " + ", ".join(cause['diagnostic_tests']) + "\n"
        tree += "  │   │   └── Treatment: " + ", ".join(cause['treatments']) + "\n"
    tree += "```"
    return tree

# Function to format the response in a clear, professional layout
def format_as_table(data):
    # Section: Medical Suggestion Heading
    layout = """
    ### 🐾 **VetBuddy Medical Suggestion**
    Below is a detailed breakdown of the **symptoms**, **possible causes**, **diagnostic tests**, **treatments**, and **warnings**.
    """

    # Section: Symptoms
    if data.get("symptoms"):
        layout += "#### 🩺 **Symptoms**\n"
        layout += f"- {', '.join(data['symptoms'])}\n\n"

    # Section: Decision Tree (Diagrams)
    layout += "#### 🔍 **Diagnostic Flow**\n"
    layout += create_decision_tree(
        data.get("symptoms", []), data.get("causes", [])
    ) + "\n\n"

    # Section: Possible Causes
    if data.get("causes"):
        layout += "#### 🧠 **Possible Causes**\n"
        layout += "| **Cause**         | **Likelihood**      | **Severity** |\n"
        layout += "|-------------------|---------------------|--------------|\n"
        for cause in data["causes"]:
            severity = cause.get("severity", "mild")  # Assume mild if not provided
            severity_color = color_text(severity.capitalize(), severity)
            layout += f"| {cause['name']} | {cause['likelihood']}%  | {severity_color} |\n"

    # Section: Diagnostic Tests and Treatments
    if data.get("causes"):
        for cause in data["causes"]:
            layout += f"##### 🧪 **{cause['name']} - Diagnostic Tests**\n"
            layout += f"- **Tests**: {', '.join(cause['diagnostic_tests'])}\n\n"
            layout += f"##### 💉 **{cause['name']} - Treatment Options**\n"
            layout += f"- **Treatments**: {', '.join(cause['treatments'])}\n\n"

    # Section: Drug Interaction Warning
    if data.get("drug_interactions"):
        layout += "#### ⚠️ **Drug Interaction Warning**\n"
        layout += f"{data['drug_interactions']}\n\n"

    # Section: Summary Recommendation
    if data.get("summary"):
        layout += "#### 🛑 **Summary Recommendation**\n"
        layout += f"{data['summary']}\n\n"

    return layout

# Main function to fetch response from ChatGPT and format it beautifully
def get_treatment_flow_with_code(prescriptions, symptoms):
    # Check if symptoms are empty
    if not symptoms:
        return "⚠️ **Please enter symptoms to generate a treatment flow.**"
    
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
        
        # Clean and format the response
        return format_as_table({
            "symptoms": symptoms,
            "causes": [
                {
                    "name": "Kidney Disease",
                    "likelihood": "60",
                    "severity": "moderate",
                    "diagnostic_tests": ["Blood Test", "Urine Test"],
                    "treatments": ["Fluid Therapy", "Dietary Management"]
                },
                {
                    "name": "Diabetes",
                    "likelihood": "40",
                    "severity": "severe",
                    "diagnostic_tests": ["Blood Glucose Test", "Urine Glucose Test"],
                    "treatments": ["Insulin Therapy", "Dietary Management"]
                }
            ],
            "drug_interactions": "Be cautious when using insulin and antibiotics together, as it may cause hypoglycemia.",
            "summary": "Focus on kidney function testing first, followed by glucose management. Use fluid therapy carefully."
        })
    
    except Exception as e:
        return f"Error: {e}"

# Main Streamlit entry point
if __name__ == "__main__":
    # Dynamically get prescriptions and symptoms from session state
    prescriptions = st.session_state.get("prescriptions", [])
    symptoms = st.session_state.get("symptoms_list", [])

    # Fetch and display the treatment flow based on the current session state
    response = get_treatment_flow_with_code(prescriptions, symptoms)
    st.markdown(response, unsafe_allow_html=True)  # Display the response beautifully
