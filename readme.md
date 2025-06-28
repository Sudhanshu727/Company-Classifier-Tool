🏢 Company Classifier Tool - Caprae Capital
This project provides a versatile tool designed to classify companies into relevant industry segments. It's built to assist Caprae Capital in quickly prioritizing leads and enhancing the SaaSquatch Leads scraping process by offering both a swift rule-based approach and a powerful AI-driven classification leveraging Google Gemini.

✨ Features
Dual Classification Modes: Choose between a traditional Keyword-Based Classifier for speed and transparency, or an advanced Gemini AI Classifier for more nuanced and accurate predictions.

Manual Company Classification: Quickly classify individual company names and descriptions entered directly into the application.

Batch Classification via CSV Upload: Upload your own CSV files containing company data for bulk classification.

Built-in Sample Data Classification: Test the tool's capabilities with a pre-loaded sample dataset.

Intelligent Description Generation: Automatically combines various company attributes (domain, year founded, industry, locality, country, LinkedIn URL) from CSV data into a single, comprehensive description for effective classification.

Leverages Existing Data: When using the Gemini AI Classifier with CSV data, it intelligently uses the existing "Industry" column from your dataset as a few-shot example to guide Gemini's predictions, significantly improving accuracy.

Performance Evaluation: For batch classifications, the tool compares the predicted industry against the "Original Industry" from your CSV, providing an accuracy score to assess performance.

User-Friendly Interface: Built with Streamlit for an interactive and intuitive web application experience.

🚀 Technologies Used
Python 3.x

Streamlit: For creating the interactive web application.

Pandas: For data manipulation and CSV handling.

python-dotenv: For securely managing environment variables (like API keys).

Google Generative AI (Gemini API): For the advanced AI-powered classification.

📁 Project Structure
company_classifier_tool/
├── .env
├── app.py
├── requirements.txt
├── data/
│ └── sample_companies.csv
└── src/
├── **init**.py
├── classifier.py
├── data_loader.py
└── llm_classifier.py

.env: Stores your GEMINI_API_KEY.

app.py: The main Streamlit application script.

requirements.txt: Lists all Python dependencies.

data/: Contains sample data, including sample_companies.csv.

src/: Core application logic.

classifier.py: Implements the keyword-based classification logic.

data_loader.py: Handles loading and preprocessing of company data.

llm_classifier.py: Manages integration with the Google Gemini API for AI-powered classification.

⚙️ Setup and Installation
Follow these steps to get the project up and running on your local machine.

1. Clone the Repository (if applicable)
   git clone <repository_url>
   cd company_classifier_tool

2. Create a Python Virtual Environment
   It's highly recommended to use a virtual environment to manage project dependencies.

python -m venv venv

3. Activate the Virtual Environment
   On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

4. Install Dependencies
   Install all required Python packages:

pip install -r requirements.txt

5. Obtain a Google Gemini API Key
   Go to the Google AI Studio to create a new API key.

Ensure your API key has access to gemini-1.5-flash or the equivalent model in your region.

6. Configure Environment Variables
   Create a file named .env in the root directory of your project (company_classifier_tool/) and add your Gemini API key:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

Replace "YOUR_API_KEY_HERE" with the actual API key you obtained. Do NOT commit this file to version control.

7. Customize Industry Categories for Gemini (Crucial for Accuracy)
   The Gemini classifier works best when it knows the exact categories it should predict.

Open src/llm_classifier.py.

Locate the allowed_industries list.

Edit this list to include all the unique industry names from your industry column in your sample_companies.csv (and any other industries you expect). This ensures Gemini classifies into your desired, predefined categories consistently.

(Optional but Recommended): Review and add more specific "few-shot examples" to the examples list in src/llm_classifier.py. These examples, ideally taken directly from your own dataset, provide Gemini with concrete instances of input-output pairs for better guidance.

▶️ How to Run the Application
Once everything is set up, run the Streamlit application from your terminal with the virtual environment activated:

streamlit run app.py

This command will open the application in your default web browser.

🚀 Usage
Select Classification Method: On the main page, choose between "Keyword-Based Classifier" or "Gemini AI Classifier".

Manual Classification: Enter a company name and a descriptive text, then click "Classify Manually Entered Company".

Upload CSV Data: Use the "Choose a CSV file" uploader to select your sample_companies.csv (or any other compatible CSV file with a name column and descriptive fields like industry, domain, etc.). Click "Classify Uploaded CSV Data".

Classify Sample Data: Click "Classify Built-in Sample Data" to process the data/sample_companies.csv included in the project.

For batch classifications, the results will be displayed in a table, showing the original industry (if available in your CSV), the predicted industry, and a confidence score. An overall accuracy score will also be presented for comparison.

🤝 Contributing
Feel free to fork this repository, contribute improvements, or suggest new features.

📄 License / Credits
Developed for the Caprae Capital AI-Readiness Pre-Screening Challenge.
Leverages Google Gemini models via the Google Generative AI Python SDK.
