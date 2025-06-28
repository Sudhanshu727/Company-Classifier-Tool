import google.generativeai as genai
import os
import streamlit as st

class GeminiCompanyClassifier:
    def __init__(self):
        self.model = None
        self._api_key_set = False

    def initialize_gemini(self):
        """Initializes the Gemini model using the API key from environment variables."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Gemini API Key not found. Please set GEMINI_API_KEY in your .env file or Streamlit secrets.")
            self._api_key_set = False
            return False
        
        try:
            genai.configure(api_key=api_key)
            
            # --- DIRECTLY USE GEMINI 1.5 FLASH ---
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            st.success("Gemini 1.5 Flash model selected and initialized.")
            # --- END OF CHANGE ---

            self._api_key_set = True
            return True
        except Exception as e:
            st.error(f"Failed to initialize Gemini API or load model. Error: {e}. Check your API key and network connection.")
            st.info("You might want to try running `for m in genai.list_models(): print(m.name)` to see available models.")
            self._api_key_set = False
            return False

    def is_initialized(self):
        return self._api_key_set and self.model is not None

    # ... (rest of your class code remains unchanged, including classify_company_gemini)

    def classify_company_gemini(self, company_name: str, description: str, existing_industry: str = None):
        """
        Classifies a company's industry using the Gemini API.
        Uses few-shot prompting to guide the model with examples.
        
        Args:
            company_name (str): The name of the company.
            description (str): A combined description of the company's details.
            existing_industry (str, optional): The industry from your dataset, if available. 
                                               Used as a positive example for few-shot prompting.

        Returns:
            tuple: (predicted_industry: str, confidence_score: float)
                   Confidence is a proxy based on Gemini's response quality/structure.
        """
        if not self.is_initialized():
            return "Error: Gemini not initialized", 0.0

        # Define some common industries the model should pick from (based on your dataset's 'Industry' column)
        allowed_industries = ['accounting', 'airlines/aviation', 'apparel & fashion', 'arts and crafts', 'automotive', 'aviation & aerospace', 'banking', 'biotechnology', 'broadcast media', 'building materials', 'business supplies and equipment', 'capital markets', 'chemicals', 'civic & social organization', 'civil engineering', 'commercial real estate', 'computer hardware', 'computer networking', 'computer software', 'construction', 'consumer electronics', 'consumer goods', 'consumer services', 'cosmetics', 'defense & space', 'design', 'education management', 'electrical/electronic manufacturing', 'entertainment', 'environmental services', 'facilities services', 'farming', 'financial services', 'food & beverages', 'food production', 'glass, ceramics & concrete', 'government administration', 'graphic design', 'health, wellness and fitness', 'higher education', 'hospital & health care', 'hospitality', 'human resources', 'individual & family services', 'industrial automation', 'information services', 'information technology and services', 'insurance', 'international affairs', 'international trade and development', 'internet', 'investment banking', 'judiciary', 'law enforcement', 'law practice', 'legal services', 'legislative office', 'leisure, travel & tourism', 'logistics and supply chain', 'luxury goods & jewelry', 'machinery', 'management consulting', 'marketing and advertising', 'mechanical or industrial engineering', 'media production', 'medical devices', 'medical practice', 'mental health care', 'military', 'mining & metals', 'motion pictures and film', 'music', 'non-profit organization management', 'oil & energy', 'outsourcing/offshoring', 'package/freight delivery', 'packaging and containers', 'paper & forest products', 'pharmaceuticals', 'philanthropy', 'photography', 'primary/secondary education', 'printing', 'professional training & coaching', 'public policy', 'public relations and communications', 'publishing', 'railroad manufacture', 'real estate', 'renewables & environment', 'research', 'restaurants', 'retail', 'security and investigations', 'semiconductors', 'sporting goods', 'staffing and recruiting', 'supermarkets', 'telecommunications', 'textiles', 'tobacco', 'translation and localization', 'transportation/trucking/railroad', 'utilities', 'wholesale', 'wine and spirits', 'wireless', 'writing and editing', 'Other']
        
        industry_list_str = ", ".join(allowed_industries)

        # Few-shot examples
        # These examples should ideally be representative of your dataset and desired output.
        # Using specific examples from your data helps Gemini align with your classification scheme.
        examples = [
            {"input": """Company: ibm. Description: Domain: ibm.com. Founded: 1911. Industry: information technology and services. Locality: new york, new york, united states. Country: united states. LinkedIn URL: linkedin.com/company/ibm.""", "output": "information technology and services"},
            {"input": """Company: us army. Description: Domain: goarmy.com. Founded: 1800. Industry: military. Locality: alexandria, virginia, united states. Country: united states. LinkedIn URL: linkedin.com/company/us-army.""", "output": "military"},
            {"input": """Company: ey. Description: Domain: ey.com. Founded: 1989. Industry: accounting. Locality: london, greater london, united kingdom. Country: united kingdom. LinkedIn URL: linkedin.com/company/ernstandyoung.""", "output": "accounting"},
            {"input": """Company: walmart. Description: Domain: walmartcareers.com. Founded: 1962. Industry: retail. Locality: withee, wisconsin, united states. Country: united states. LinkedIn URL: linkedin.com/company/walmart.""", "output": "retail"},
            {"input": """Company: microsoft. Description: Domain: microsoft.com. Founded: 1975. Industry: computer software. Locality: redmond, washington, united states. Country: united states. LinkedIn URL: linkedin.com/company/microsoft.""", "output": "computer software"},
        ]

        # Add an example from the actual company's existing industry if available
        # This acts as a strong hint for few-shot learning
        if existing_industry and existing_industry.strip() and existing_industry != "Other":
            # Ensure the example is clean and relevant to Gemini's internal knowledge
            example_description = f"Company: {company_name}. Description: {description}"
            # Avoid adding duplicate examples if the existing_industry matches one of the hardcoded ones exactly
            if not any(ex['output'].lower() == existing_industry.lower() for ex in examples):
                examples.insert(0, {"input": example_description, "output": existing_industry.strip()})


        prompt = f"""
        You are an expert industry classifier. Your task is to classify companies into one of the following predefined industry categories: {industry_list_str}.

        Examples:
        """
        for ex in examples:
            prompt += f"Input: {ex['input']}\nOutput: {ex['output']}\n"
        
        prompt += f"""
        Classify the following company into the most relevant category from the provided list.
        Company: {company_name}. Description: {description}
        Output:
        """

        try:
            response = self.model.generate_content(prompt, generation_config={"temperature": 0.0}) # Low temperature for consistent classification
            
            # Extracting predicted industry from response
            # Gemini might add extra text, so we need to be robust
            predicted_industry = response.text.strip()
            
            # Basic validation/cleaning
            # Check if the predicted industry is one of the allowed ones, or similar enough
            found_match = False
            final_predicted_industry = "Other" # Default if no strong match
            for allowed in allowed_industries:
                if allowed.lower() == predicted_industry.lower():
                    final_predicted_industry = allowed
                    found_match = True
                    break
                # Simple substring match for robustness (e.g., if Gemini says "IT Services" for "Information Technology and Services")
                if allowed.lower() in predicted_industry.lower() or predicted_industry.lower() in allowed.lower():
                    final_predicted_industry = allowed
                    found_match = True
                    break
            
            # Simple confidence: 1.0 if it's a known category, 0.5 if 'Other' or unexpected.
            confidence = 1.0 if found_match else 0.5 

            return final_predicted_industry, confidence

        except Exception as e:
            st.error(f"Gemini API call failed for {company_name}. Error: {e}")
            return "Error (API Failed)", 0.0

# Initialize the classifier globally or when needed in app.py
gemini_classifier = GeminiCompanyClassifier()

if __name__ == '__main__':
    # Test cases (ensure you have your GEMINI_API_KEY set in .env)
    os.environ["GEMINI_API_KEY"] = "YOUR_TEST_API_KEY" # Replace with a dummy for local test
    
    if gemini_classifier.initialize_gemini():
        print("Gemini Classifier Initialized. Running tests...")
        
        # Test cases for Gemini (using some examples from the generated list)
        test_companies = [
            {"name": "IBM", "desc": "Domain: ibm.com. Founded: 1911. Industry: information technology and services. Locality: new york, new york, united states. Country: united states. LinkedIn URL: linkedin.com/company/ibm.", "actual_industry": "information technology and services"},
            {"name": "US Army", "desc": "Domain: goarmy.com. Founded: 1800. Industry: military. Locality: alexandria, virginia, united states. Country: united states. LinkedIn: linkedin.com/company/us-army.", "actual_industry": "military"},
            {"name": "EY", "desc": "Domain: ey.com. Founded: 1989. Industry: accounting. Locality: london, greater london, united kingdom. Country: united kingdom. LinkedIn: linkedin.com/company/ernstandyoung.", "actual_industry": "accounting"},
            {"name": "Reliance Industries Limited", "desc": "Domain: ril.com. Founded: 1966. Industry: oil & energy. Locality: mumbai, maharashtra, india. Country: india. LinkedIn: linkedin.com/company/reliance-industries-limited.", "actual_industry": "oil & energy"}
        ]

        for company in test_companies:
            predicted_industry, confidence = gemini_classifier.classify_company_gemini(
                company['name'], 
                company['desc'], 
                existing_industry=company['actual_industry']
            )
            print(f"Company: {company['name']}")
            print(f"  Actual Industry: {company['actual_industry']}")
            print(f"  Gemini Predicted: {predicted_industry} (Confidence: {confidence:.2f})")
            print("-" * 30)
    else:
        print("Gemini Classifier NOT Initialized. Cannot run tests.")