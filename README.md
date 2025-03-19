# Alkaike-Tech

**Setting Up and Running the Company Sentiment Analyzer**

### Prerequisites
Ensure you have the following installed on your system:

- **Python**: Version 3.7 or later. Download it from [python.org](https://www.python.org/downloads/).

### Environment Variables
Create a `.env` file in the root directory and add the required API keys:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
ELEVEN_LABS_API_KEY =your_elevnlabs_api_key 
```

### Installation
1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set Up a Virtual Environment**

   It's best to use a virtual environment to manage dependencies.

   - On **Windows**:

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

   - On **macOS/Linux**:

     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Install Python Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the FastAPI Server**

   ```bash
   uvicorn api:app --reload
   ```

   This will start the FastAPI server at [http://localhost:8000](http://localhost:8000).

2. **Run the Streamlit App**

   Open a new terminal window and launch the Streamlit app:

   ```bash
   streamlit run app.py --server.port 8080
   ```

   This will open the application in your default web browser.

### Usage

1. Enter the company name and select the model provider in the Streamlit app.
2. Click on **"Fetch Sentiment Data"** to analyze sentiment data for the specified company.

### Notes

- Ensure your `.env` file is correctly configured with the necessary API keys.
- An active internet connection is required as the application relies on external APIs.
- If you encounter any issues, check the console output for errors and verify all dependencies are installed correctly.


