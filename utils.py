from typing import Literal
from tavily import TavilyClient
from pydantic import BaseModel
from ollama import chat
from typing import Literal

def fetch_from_web(query):
    tavily_client = TavilyClient(api_key="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")
    response = tavily_client.search(query, include_raw_content=True, max_results=10 , topic="news" , search_depth="basic")
    return {"sources": response['results']}

class Sentiment(BaseModel):
    summary: str
    reasoning: str
    topics: list[str]
    sentiment: Literal['positive', 'negative', 'neutral']

def analyze_sentiment(article):
    
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': f"""
                Analyze the following news article about a company:

                1. **Summary**: Provide a comprehensive summary of the article's key points.
                
                2. **Sentiment Analysis**: 
                - Classify the overall sentiment toward the company as: POSITIVE, NEGATIVE, or NEUTRAL
                - Support your classification with specific quotes, tone analysis, and factual evidence from the article
                - Explain your reasoning for this sentiment classification
                
                3. **Key Topics**: 
                - Identify 3-5 main topics discussed in the article
                - Only give the name of the topics

                Be as detailed and objective as possible in your reasoning.

                Article Title: {article['title']}

                Article: {article['raw_content']}
                """
            }
        ],
        model='llama3.2:3b',
        format=Sentiment.model_json_schema(),
    )

    try:
    
        sentiment_output = Sentiment.model_validate_json(response.message.content)

        return {
            "title" : article["title"],
            "summary": sentiment_output.summary,
            "reasoning": sentiment_output.reasoning,
            "topics": sentiment_output.topics,
            "sentiment": sentiment_output.sentiment
        }

    except Exception as e:
        print(f"Error parsing sentiment output: {e}")
        return None
    
