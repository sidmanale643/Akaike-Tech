from fastapi import FastAPI
from utils import fetch_from_web, analyze_sentiment, generate_comparative_sentiment, generate_final_report, get_summaries_by_sentiment, translate , text_to_speech

app = FastAPI()

@app.get("/home")
def main(company_name: str , model_provider : str):
    web_results = fetch_from_web(company_name)
    
    if 'sources' not in web_results:
        return {"error": "No sources found."}

    sentiment_output = [analyze_sentiment(article , model_provider) for article in web_results['sources'][:5]]
    
    comparative_sentiment = generate_comparative_sentiment(sentiment_output)

    positive_summary, negative_summary, neutral_summary = get_summaries_by_sentiment(sentiment_output)

    final_report = generate_final_report(positive_summary, negative_summary, neutral_summary, comparative_sentiment , model_provider)
    hindi_translation = translate(final_report , model_provider)

    audio_path = text_to_speech(hindi_translation)

    return {
        "company_name": company_name,
        "articles": sentiment_output,
        "comparative_sentiment": comparative_sentiment,
        "final_report": final_report,
        "hindi_translation": hindi_translation,
        "audio_url": audio_path
    }
