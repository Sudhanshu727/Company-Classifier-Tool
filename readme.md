# 🏢 **Company Classifier Tool – Caprae Capital**

This project provides a versatile tool designed to classify companies into relevant industry segments. It's built to assist **Caprae Capital** in quickly prioritizing leads and enhancing the **SaaSquatch Leads** scraping process by offering both a swift rule-based approach and a powerful AI-driven classification leveraging **Google Gemini**.

---

## ✨ **Features**

* **Dual Classification Modes**
  Choose between a traditional **Keyword-Based Classifier** for speed and transparency, or an advanced **Gemini AI Classifier** for more nuanced and accurate predictions.

* **Manual Company Classification**
  Quickly classify individual company names and descriptions entered directly into the application.

* **Batch Classification via CSV Upload**
  Upload your own CSV files containing company data for bulk classification.

* **Built-in Sample Data Classification**
  Test the tool's capabilities with a pre-loaded sample dataset.

* **Intelligent Description Generation**
  Automatically combines various company attributes (domain, year founded, industry, locality, country, LinkedIn URL) from CSV data into a single, comprehensive description for effective classification.

* **Leverages Existing Data**
  When using the Gemini AI Classifier with CSV data, it intelligently uses the existing **"Industry"** column from your dataset as a **few-shot example** to guide Gemini's predictions, significantly improving accuracy.

* **Performance Evaluation**
  For batch classifications, the tool compares the predicted industry against the **"Original Industry"** from your CSV, providing an accuracy score to assess performance.

* **User-Friendly Interface**
  Built with **Streamlit** for an interactive and intuitive web application experience.

---

## 🚀 **Technologies Used**

* **Python 3.x**
* **Streamlit** – For creating the interactive web application.
* **Pandas** – For data manipulation and CSV handling.
* **python-dotenv** – For securely managing environment variables (like API keys).
* **Google Generative AI (Gemini API)** – For the advanced AI-powered classification.

---

## 📁 **Project Structure**

```
company_classifier_tool/
├── .env
├── app.py
├── requirements.txt
├── data/
│   └── sample_companies.csv
└── src/
    ├── __init__.py
    ├── classifier.py
    ├── data_loader.py
    └── llm_classifier.py
```

* **.env**: Stores your `GEMINI_API_KEY`.
* **app.py**: The main Streamlit application script.
* **requirements.txt**: Lists all Python dependencies.
* **data/**: Contains sample data, including `sample_companies.csv`.
* **src/**: Core application logic:

  * `classifier.py`: Implements the keyword-based classification logic.
  * `data_loader.py`: Handles loading and preprocessing of company data.
  * `llm_classifier.py`: Manages integration with the Google Gemini API for AI-powered classification.

---

## ⚙️ **Setup and Installation**

### 1. **Clone the Repository**

```bash
git clone <repository_url>
cd company_classifier_tool
```

### 2. **Create a Python Virtual Environment**

```bash
python -m venv venv
```

### 3. **Activate the Virtual Environment**

* On **Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

* On **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 5. **Obtain a Google Gemini API Key**

* Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to create an API key.
* Ensure your key has access to **gemini-1.5-flash** or the appropriate model.

### 6. **Configure Environment Variables**

Create a file named `.env` in the root of your project:

```env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

> **Do NOT commit this file** to version control.

### 7. **Customize Industry Categories for Gemini (Crucial for Accuracy)**

* Open `src/llm_classifier.py`
* Locate the `allowed_industries` list and update it to match all unique industry labels from your dataset.
* (Optional but Recommended): Add more specific **few-shot examples** to the `examples` list to improve Gemini's contextual accuracy.

---

## ▶️ **How to Run the Application**

Once set up, launch the Streamlit app with:

```bash
streamlit run app.py
```

This will open the application in your default web browser.

---

## 🚀 **Usage**

1. **Select Classification Method**
   Choose between **Keyword-Based Classifier** or **Gemini AI Classifier**.

2. **Manual Classification**
   Enter a company name and description, then click **Classify Manually Entered Company**.

3. **Upload CSV Data**
   Upload your CSV (e.g., `sample_companies.csv`) containing company descriptions or features. Click **Classify Uploaded CSV Data**.

4. **Classify Sample Data**
   Use the built-in example in `/data/sample_companies.csv` by clicking **Classify Built-in Sample Data**.

> For batch classification, results will include:
>
> * Original Industry (if provided)
> * Predicted Industry
> * Confidence Score
> * Overall Accuracy Score (if applicable)

---

## 🤝 **Contributing**

Feel free to fork this repository, contribute improvements, or suggest new features. All contributions are welcome.

---

## 📄 **License / Credits**

* Developed for the **Caprae Capital AI-Readiness Pre-Screening Challenge**.
* Leverages **Google Gemini models** via the **Google Generative AI Python SDK**.

---
