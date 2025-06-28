import pandas as pd
import re

def classify_company_keyword_based(company_name: str, description: str):
    """
    Classifies a company into a relevant industry label using keyword-based rules.
    Also provides a simple confidence score.

    Args:
        company_name (str): The name of the company.
        description (str): The description of the company (can be combined from multiple fields).

    Returns:
        tuple: (industry_label: str, confidence_score: float)
    """
    text = (company_name + " " + description).lower()
    
    # Define keywords for different industries
    # These keywords are designed to be relevant to common tech/startup segments.
    # You can expand or refine these based on Caprae Capital's specific focus areas.
    industry_keywords = {
        "SaaS": ["saas", "software as a service", "cloud software", "subscription-based software", "platform as a service", "crm", "erp", "hr software", "marketing automation", "enterprise software"],
        "FinTech": ["fintech", "finance technology", "payment", "banking", "lending", "investment", "blockchain", "cryptocurrency", "financial services", "insurtech"],
        "EdTech": ["edtech", "education technology", "e-learning", "online learning", "course platform", "educational software", "school management", "learning management system"],
        "HealthTech": ["healthtech", "healthcare technology", "medical devices", "biotech", "pharmaceutical", "digital health", " telehealth", "health data", "medtech", "diagnostics"],
        "AI/ML": ["ai", "artificial intelligence", "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "data science", "predictive analytics", "generative ai", "neural networks"],
        "Cybersecurity": ["cybersecurity", "security software", "threat intelligence", "data protection", "network security", "endpoint security", "firewall", "infosec"],
        "E-commerce": ["e-commerce", "online retail", "marketplace", "shopify", "digital storefront", "retail tech", "online shopping"],
        "HR Tech": ["hr tech", "human resources software", "recruitment platform", "talent management", "payroll software", "workforce management"],
        "Marketing Tech": ["martech", "marketing technology", "adtech", "advertising technology", "crm", "marketing automation", "sales enablement"],
        "PropTech": ["proptech", "real estate technology", "property management software", "smart building", "construction tech"],
        "LegalTech": ["legaltech", "legal software", "legal practice management", "e-discovery", "legal AI"],
        "Agritech": ["agritech", "agriculture technology", "precision farming", "farm management", "crop science", "foodtech"],
        "Logistics Tech": ["logistics tech", "supply chain management", "transportation software", "fleet management"],
        "Automotive Tech": ["automotive tech", "electric vehicles", "autonomous driving", "vehicle software"],
        "CleanTech": ["cleantech", "renewable energy", "sustainability", "environmental technology", "waste management"],
        "Gaming": ["gaming", "game development", "esports", "interactive entertainment"],
        "Media & Entertainment": ["media tech", "streaming platform", "content creation", "digital media", "broadcasting"],
        "Biotechnology": ["biotech", "biotechnology", "life sciences", "genomics", "drug discovery"],
        "Consulting": ["consulting", "advisory services", "strategy consulting", "business services"], # Added based on IBM/TCS examples
        "Manufacturing": ["manufacturing", "industrial", "robotics", "automation", "production"],
        "IT Services": ["information technology and services", "it services", "managed services", "software development services", "system integration"] # Specific for IBM/TCS
    }

    # Normalize text for better matching (optional, but good practice)
    # Remove characters that are not letters, numbers, or spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text) 
    text_words = set(text.split()) # Use a set for faster lookups

    matched_industries = {}
    for industry, keywords in industry_keywords.items():
        score = 0
        for keyword in keywords:
            # Check if the keyword (or phrase) is present in the cleaned text
            if keyword in text:
                score += text.count(keyword) # Count occurrences for a stronger signal
        if score > 0:
            matched_industries[industry] = score

    if not matched_industries:
        return "Other", 0.0

    # Determine the best match and calculate a simple confidence score
    # Confidence is based on the number of matched keywords relative to the potential maximum for that industry
    
    # Sort by score in descending order
    sorted_matches = sorted(matched_industries.items(), key=lambda item: item[1], reverse=True)
    
    best_industry = sorted_matches[0][0]
    best_score = sorted_matches[0][1]

    # Simple confidence: proportion of matched keywords for the best industry
    # Sum of counts for the best industry divided by the sum of counts across all keywords for that industry
    total_possible_score_for_best_industry = sum(text.count(kw) for kw in industry_keywords[best_industry] if kw in text)
    if total_possible_score_for_best_industry == 0: # Should not happen if best_score > 0
        confidence = 0.0
    else:
        confidence = best_score / total_possible_score_for_best_industry
    
    # If the exact 'industry' from your CSV matches a primary keyword of a category, boost confidence
    original_industry_from_csv = description.lower() # Assuming 'description' contains 'industry' from your CSV
    if best_industry.lower() in original_industry_from_csv or original_industry_from_csv in best_industry.lower():
         confidence = min(confidence + 0.2, 1.0) # Add a small boost, cap at 1.0

    confidence = min(confidence, 1.0) # Ensure confidence doesn't exceed 1.0
    
    return best_industry, round(confidence, 2)

if __name__ == '__main__':
    # Simple tests when run directly
    print("--- Testing Keyword Classifier ---")
    print(classify_company_keyword_based("IBM", "Domain: ibm.com. Founded: 1911. Industry: information technology and services. Locality: new york, new york, united states. Country: united states. LinkedIn: linkedin.com/company/ibm.")) # Should be IT Services/Consulting
    print(classify_company_keyword_based("Tata Consultancy Services", "Domain: tcs.com. Founded: 1968. Industry: information technology and services. Locality: bombay, maharashtra, india. Country: india. LinkedIn: linkedin.com/company/tata-consultancy-services.")) # Should be IT Services/Consulting
    print(classify_company_keyword_based("Acme EdTech", "Domain: acmeed.com. Founded: 2020. Industry: Education Technology. Locality: San Francisco. Country: USA.")) # Should be EdTech
    print(classify_company_keyword_based("Global Manufacturing Inc.", "Manufactures industrial machinery and heavy equipment.")) # Should be Manufacturing
    print(classify_company_keyword_based("HealthMind AI", "Utilizes artificial intelligence for predictive analytics in healthcare and medical research.")) # Should be AI/ML or HealthTech
    print(classify_company_keyword_based("Quantum Robotics", "Designs and manufactures advanced robotics and automation systems for industrial use.")) # Should be Manufacturing or AI/ML
    print(classify_company_keyword_based("No matching keywords found company", "This is a generic description for a company."))