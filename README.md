Company Sentiment Analyzer

**Setting Up and Running the Company Sentiment Analyzer**

### Prerequisites
Ensure you have the following installed on your system:

- **Python**: Version 3.7 or later. Download it from [python.org](https://www.python.org/downloads/).

### Environment Variables
Create a `.env` file in the root directory and add the required API keys:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
ELEVEN_LABS_API_KEY =your_elevenlabs_api_key 
```

### Installation
1. **Clone the Repository**

   ```bash
   git clone https://github.com/sidmanale643/Company-Sentiment-Analyzer.git
   cd Company-Sentiment-Analyzer
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

### API Usage

The provided codebase primarily consists of a FastAPI application (`api.py`) and a Streamlit application (`app.py`). Here's a breakdown of how the APIs are being used:

#### FastAPI Application (`api.py`)

- **Endpoint**: `/home`
- **Method**: `GET`

**Parameters:**
- `company_name`: The name of the company for which sentiment analysis is to be performed.
- `model_provider`: The provider of the sentiment analysis model, either "Ollama" or "Groq".
- `tts_provider`: The provider of the TextToSpeech model.

**Functionality:**
- Fetches news articles related to the specified company.
- Analyzes the sentiment of these articles using the specified model provider.
- Generates a comparative sentiment analysis and a final report.
- Translates the report into Hindi and converts it to speech.

**Response:**
Returns a JSON object containing:
- Company name
- Sentiment analysis results
- Comparative sentiment
- Final report
- Hindi translation
- Audio File URL

#### Streamlit Application (`app.py`)

- Acts as a front-end interface for users to input the company name and select a model provider.
- Sends a request to the FastAPI endpoint to fetch sentiment data.
- Displays the results, including the final report and audio output.

### OpenSource TextToSpeech Model

**Indic Parler TTS**

- Multilingual Support: Generates natural-sounding speech in 21 languages, including 20 Indic languages and English.
- Customizable Voices: Offers 69 unique voices with options to adjust background noise, pitch, and speaking rate.
- Open-Source: Developed by Hugging Face and AI4Bharat, licensed under Apache 2.0.

### Third-Party APIs

1. **Tavily API**
   - **Purpose**: Fetches news articles related to a company.
   - **Integration**: Utilized in the `fetch_from_web` function in `utils.py` using the `TavilyClient`.

2. **Ollama and Groq APIs**
   - **Purpose**: Perform sentiment analysis and generate reports.
   - **Integration**: Used in the `analyze_sentiment`, `generate_final_report`, and `translate` functions in `utils.py`.

3. **Eleven Labs API**
   - **Purpose**: Converts text to speech.
   - **Integration**: Used in the `text_to_speech` function in `utils.py`.

### Accessing the API via Postman

To access the FastAPI endpoint using Postman:

1. Open Postman and create a new request.
2. Set the request type to `GET`.
3. Enter the URL:

   ```
   http://localhost:8000/home?company_name=Tesla&model_provider=Ollama&tts_provider=ElevenLabs
   ```

   Replace `Tesla` , `Ollama` and `ElevenLabs` with your desired values.

4. Send the request and view the response in the Postman interface.

### Assumptions & Limitations

**Assumptions:**
- The Tavily API key is correctly set in the environment variables.
- The model providers "Ollama" and "Groq" are available and correctly configured.
- A GPU is available for the TTS model to be used.
- The Eleven Labs API key is valid and has the necessary permissions.

**Limitations:**
- Currently disabled the "Comparative Analysis Functionality" to reduce overall prompt sizes.
- CPU performance is extremely slow.
- The current implementation uses the Llama 3.2 3B model, a smaller model chosen due to GPU unavailability. Performance is expected to improve significantly with a larger model or with Groq PRO Tier.
- The sentiment analysis is limited to the first 5 articles fetched because of rate limits imposed by Groq Free Tier.
- A third-party API is used for text-to-speech instead of a custom open-source model (e.g., Indic-Parler TTS) due to the unavailability of a GPU on Hugging Face Spaces.
- The text-to-speech functionality depends on the Eleven Labs API, which may have rate limits or require a subscription.
- The translation and sentiment analysis rely on the accuracy and availability of the respective APIs.

### Notes

- Ensure your `.env` file is correctly configured with the necessary API keys.
- An active internet connection is required as the application relies on external APIs.
- If you encounter any issues, check the console output for errors and verify all dependencies are installed correctly.



