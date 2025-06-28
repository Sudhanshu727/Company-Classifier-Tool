import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv # For loading .env file locally

# Load environment variables from .env file (for local development)
load_dotenv()

# Import classifier and data loader
from src.classifier import classify_company_keyword_based # Your existing keyword classifier
from src.llm_classifier import gemini_classifier          # Your new Gemini classifier instance
from src.data_loader import load_sample_companies, load_custom_companies

# --- Page Configuration ---
st.set_page_config(
    page_title="Company Classifier Tool - Caprae Capital",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.title("🏢 Company Classifier Tool")
st.markdown("""
    This tool classifies company names and descriptions into relevant industry segments.
    It aims to help Caprae Capital quickly prioritize leads and enhance the **SaaSquatch Leads** scraping tool
    by leveraging either rule-based logic or advanced AI (Gemini).
""")

# --- Sidebar for About and Instructions ---
with st.sidebar:
    st.header("About This Tool")
    st.info("""
        This application demonstrates two approaches to company classification:
        1.  **Keyword-Based:** Simple, fast, and relies on predefined rules.
        2.  **Gemini AI-Based:** Leverages Google's powerful LLM for more nuanced and accurate classifications, especially with few-shot prompting using your existing 'Industry' data.

        **Tech Stack:** Python, Streamlit, Pandas, Keyword Logic, Google Gemini API.
    """)
    st.header("How to Use")
    st.markdown("""
    1.  **Select Classifier:** Choose 'Keyword-Based' or 'Gemini AI'.
    2.  **Manual Entry:** Type company details and classify.
    3.  **Upload CSV:** Upload your own CSV file with company data. Ensure it has a 'name' column and other descriptive columns like 'domain', 'industry', etc.
    4.  **Load Sample Data:** Classify built-in sample companies.
    """)
    
    st.subheader("Gemini API Key Status")
    # Initialize Gemini classifier here to check key status and for use throughout the app
    if not gemini_classifier.is_initialized():
        if gemini_classifier.initialize_gemini():
            st.success("Gemini API Initialized Successfully!")
        else:
            st.warning("Gemini API Key NOT found or initialization failed. Gemini classifier will not work.")
    else:
        st.success("Gemini API is ready to use!")


# --- Classifier Selection ---
st.header("Choose Classification Method")
classification_method = st.radio(
    "Select the classifier you want to use:",
    ("Keyword-Based Classifier", "Gemini AI Classifier"),
    help="Keyword-based is faster but less flexible. Gemini AI is more powerful but requires an API key."
)

# --- Manual Classification Section ---
st.header("1. Manual Company Classification")
col1, col2 = st.columns(2)
with col1:
    company_name_input = st.text_input("Enter Company Name", placeholder="e.g., Innovate Software Inc.")
with col2:
    company_description_input = st.text_area("Enter Company Description", placeholder="e.g., Develops cloud-native SaaS solutions for data analytics or similar verbose text.", height=100)

if st.button("Classify Manually Entered Company", help="Click to classify the manually entered company"):
    if company_name_input and company_description_input:
        with st.spinner("Classifying..."):
            if classification_method == "Keyword-Based Classifier":
                industry, confidence = classify_company_keyword_based(company_name_input, company_description_input)
            elif classification_method == "Gemini AI Classifier":
                if gemini_classifier.is_initialized():
                    industry, confidence = gemini_classifier.classify_company_gemini(company_name_input, company_description_input)
                else:
                    st.error("Gemini AI Classifier is not initialized. Please check API key.")
                    industry, confidence = "Error", 0.0
            
            if industry != "Error":
                st.success("Classification Complete!")
                st.write(f"**Company Name:** {company_name_input}")
                st.write(f"**Description:** {company_description_input}")
                st.markdown(f"**Predicted Industry:** <span style='font-size: 1.2em; color: #28a745;'>**`{industry}`**</span>", unsafe_allow_html=True)
                st.write(f"**Confidence Score:** `{confidence:.2f}`")
            else:
                st.error("Classification failed. Please check messages above.")
    else:
        st.warning("Please enter both company name and description to classify.")

st.markdown("---")

# --- Batch Classification Section (for Uploaded CSV and Sample Data) ---
st.header("2. Classify Uploaded Company Data (CSV)")
st.info(f"""
    Upload a CSV file containing your company data.
    It must have a column named **`name`** for the company name.
    Other columns like **`domain`, `year founded`, `industry`, `locality`, `country`, `linkedin url`**
    will be combined to form a rich description for classification.
    The existing 'Industry' column (if present) will be used by the **{classification_method}** for better classification.
""")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="Upload a CSV with 'name' and other descriptive columns as specified.")

if uploaded_file is not None:
    if st.button("Classify Uploaded CSV Data", help="Load and classify companies from your uploaded CSV"):
        with st.spinner("Loading and classifying uploaded data..."):
            # Load data, including the original 'industry' column
            custom_df = load_custom_companies(uploaded_file)
            
            if not custom_df.empty:
                st.write(f"### Classifying Uploaded Companies using {classification_method}:")
                uploaded_results = []
                correct_predictions = 0
                total_predictions = 0

                for index, row in custom_df.iterrows():
                    company_name = row['company_name']
                    description = row['description'] # This is the combined description generated by data_loader
                    original_industry = row['original_industry'] # This is the existing industry from your CSV

                    predicted_industry = "N/A"
                    confidence = 0.0

                    if classification_method == "Keyword-Based Classifier":
                        predicted_industry, confidence = classify_company_keyword_based(company_name, description)
                    elif classification_method == "Gemini AI Classifier":
                        if gemini_classifier.is_initialized():
                            predicted_industry, confidence = gemini_classifier.classify_company_gemini(
                                company_name, description, existing_industry=original_industry
                            )
                        else:
                            st.error("Gemini AI Classifier not initialized. Cannot classify with Gemini.")
                            predicted_industry, confidence = "Error (Gemini not ready)", 0.0
                    
                    # Store results
                    result_row = {
                        "Company Name": company_name,
                        "Derived Description (for Classifier)": description,
                        "Original Industry (from CSV)": original_industry, # Display original for comparison
                        "Predicted Industry": predicted_industry,
                        "Confidence Score": f"{confidence:.2f}"
                    }
                    uploaded_results.append(result_row)

                    # For accuracy calculation (only if original_industry is available and not N/A)
                    if original_industry != 'N/A' and predicted_industry != "N/A" and predicted_industry != "Error (Gemini not ready)":
                        total_predictions += 1
                        # Simple accuracy check: direct string match (case-insensitive for robustness)
                        if predicted_industry.lower() == original_industry.lower():
                            correct_predictions += 1
                        # Add a fuzzy match for "information technology and services" and "IT Services"
                        elif (("information technology and services" in original_industry.lower() or "it services" in original_industry.lower()) and 
                              ("information technology and services" in predicted_industry.lower() or "it services" in predicted_industry.lower())):
                            correct_predictions += 1

                uploaded_results_df = pd.DataFrame(uploaded_results)
                st.dataframe(uploaded_results_df, use_container_width=True)

                if total_predictions > 0:
                    accuracy = (correct_predictions / total_predictions) * 100
                    st.success(f"**Classification Accuracy (against 'Original Industry' in CSV): {accuracy:.2f}%** "
                               f"({correct_predictions} out of {total_predictions} classified companies match)")
                else:
                    st.info("No companies with original industry labels were processed for accuracy calculation.")
            else:
                st.error("Could not process the uploaded CSV. Please ensure the file is valid and contains the required 'name' column.")

st.markdown("---")

st.header("3. Classify Built-in Sample Companies")
st.write("Click the button below to classify a small sample dataset that comes with the tool.")

if st.button("Classify Built-in Sample Data", help="Load and classify companies from the built-in sample data file"):
    sample_df = load_sample_companies()
    if not sample_df.empty:
        st.write(f"### Classifying Built-in Sample Companies using {classification_method}:")
        results = []
        correct_predictions = 0
        total_predictions = 0

        for index, row in sample_df.iterrows():
            company_name = row['company_name']
            description = row['description']
            original_industry = row['original_industry']

            predicted_industry = "N/A"
            confidence = 0.0

            if classification_method == "Keyword-Based Classifier":
                predicted_industry, confidence = classify_company_keyword_based(company_name, description)
            elif classification_method == "Gemini AI Classifier":
                if gemini_classifier.is_initialized():
                    predicted_industry, confidence = gemini_classifier.classify_company_gemini(
                        company_name, description, existing_industry=original_industry
                    )
                else:
                    st.error("Gemini AI Classifier not initialized. Cannot classify with Gemini.")
                    predicted_industry, confidence = "Error (Gemini not ready)", 0.0
            
            # Store results
            result_row = {
                "Company Name": company_name,
                "Derived Description (for Classifier)": description,
                "Original Industry (from CSV)": original_industry,
                "Predicted Industry": predicted_industry,
                "Confidence Score": f"{confidence:.2f}"
            }
            results.append(result_row)

            # For accuracy calculation
            if original_industry != 'N/A' and predicted_industry != "N/A" and predicted_industry != "Error (Gemini not ready)":
                total_predictions += 1
                if predicted_industry.lower() == original_industry.lower():
                    correct_predictions += 1
                elif (("information technology and services" in original_industry.lower() or "it services" in original_industry.lower()) and 
                      ("information technology and services" in predicted_industry.lower() or "it services" in predicted_industry.lower())):
                    correct_predictions += 1


        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True)

        if total_predictions > 0:
            accuracy = (correct_predictions / total_predictions) * 100
            st.success(f"**Classification Accuracy (against 'Original Industry' in CSV): {accuracy:.2f}%** "
                       f"({correct_predictions} out of {total_predictions} classified companies match)")
        else:
            st.info("No companies with original industry labels were processed for accuracy calculation.")
    else:
        st.error("Could not load built-in sample data. Please check 'data/sample_companies.csv' and its content.")

st.markdown("---")
st.caption("Developed for the Caprae Capital AI-Readiness Pre-Screening Challenge.")