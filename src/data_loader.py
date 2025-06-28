import pandas as pd
import os
import streamlit as st # Import streamlit for st.error/st.warning messages

def combine_columns_to_description(row, columns_to_combine):
    """
    Combines values from specified columns into a single descriptive string.
    Handles potential NaN values by converting them to empty strings.
    Adds labels to make the description more informative for NLP.
    """
    formatted_parts = []
    
    # Iterate through specified columns and add them with labels if present and not empty
    if 'domain' in columns_to_combine and 'domain' in row.index and pd.notna(row['domain']) and str(row['domain']).strip() != '':
        formatted_parts.append(f"Domain: {str(row['domain']).strip()}")
    if 'year founded' in columns_to_combine and 'year founded' in row.index and pd.notna(row['year founded']) and str(row['year founded']).strip() != '':
        formatted_parts.append(f"Founded: {str(row['year founded']).strip()}")
    if 'industry' in columns_to_combine and 'industry' in row.index and pd.notna(row['industry']) and str(row['industry']).strip() != '':
        formatted_parts.append(f"Industry: {str(row['industry']).strip()}")
    if 'locality' in columns_to_combine and 'locality' in row.index and pd.notna(row['locality']) and str(row['locality']).strip() != '':
        formatted_parts.append(f"Locality: {str(row['locality']).strip()}")
    if 'country' in columns_to_combine and 'country' in row.index and pd.notna(row['country']) and str(row['country']).strip() != '':
        formatted_parts.append(f"Country: {str(row['country']).strip()}")
    if 'linkedin url' in columns_to_combine and 'linkedin url' in row.index and pd.notna(row['linkedin url']) and str(row['linkedin url']).strip() != '':
        formatted_parts.append(f"LinkedIn URL: {str(row['linkedin url']).strip()}")

    # Join with a period and space for better readability and separation for NLP
    return ". ".join(formatted_parts) + "." if formatted_parts else ""


def load_company_data(filepath, is_sample=True):
    """
    Loads company data from a CSV file, creates a combined description,
    and returns relevant columns including the original 'industry' if available.

    Args:
        filepath (str): Path to the CSV file.
        is_sample (bool): True if loading sample data, False if from uploaded file object.

    Returns:
        pd.DataFrame: DataFrame with 'company_name', 'description', and 'original_industry'.
                      Returns empty DataFrame on error or if essential columns are missing.
    """
    try:
        if is_sample:
            if not os.path.exists(filepath):
                print(f"Error: Sample data file not found at {filepath}")
                return pd.DataFrame(columns=['company_name', 'description', 'original_industry'])
            df = pd.read_csv(filepath)
        else: # For uploaded file, filepath is the file object
            df = pd.read_csv(filepath)
        
        # Check for 'name' column as company name
        if 'name' not in df.columns:
            st.error("Error: The CSV must contain a column named 'name' for the company name.")
            return pd.DataFrame(columns=['company_name', 'description', 'original_industry'])

        # Define columns to combine into the 'description' for the classifier
        descriptive_cols = ['domain', 'year founded', 'industry', 'locality', 'country', 'linkedin url']
        
        # Filter for columns that actually exist in the CSV
        existing_descriptive_cols = [col for col in descriptive_cols if col in df.columns]
        
        if not existing_descriptive_cols:
            st.warning("Warning: No suitable descriptive columns found (domain, year founded, etc.) to create a rich description. "
                       "Classification might be less accurate for this data.")
            df['description'] = ''
        else:
            df['description'] = df.apply(lambda row: combine_columns_to_description(row, existing_descriptive_cols), axis=1)
            
        # Rename 'name' to 'company_name' for consistency
        df.rename(columns={'name': 'company_name'}, inplace=True)

        # Store the original 'industry' column if it exists
        df['original_industry'] = df['industry'].fillna('N/A') if 'industry' in df.columns else 'N/A'
        
        return df[['company_name', 'description', 'original_industry']]

    except Exception as e:
        st.error(f"Error loading data: {e}. Please ensure it's a valid CSV file.")
        return pd.DataFrame(columns=['company_name', 'description', 'original_industry'])

# Helper functions for app.py to call
def load_sample_companies(filepath='data/sample_companies.csv'):
    return load_company_data(filepath, is_sample=True)

def load_custom_companies(uploaded_file):
    return load_company_data(uploaded_file, is_sample=False)

if __name__ == '__main__':
    # Simple test for sample data loading
    sample_df = load_sample_companies()
    print("Sample Data Loaded (with original_industry):")
    print(sample_df.head())