import os
from typing import Literal
from tavily import TavilyClient
from pydantic import BaseModel
from ollama import chat
from typing import Literal
from dotenv import load_dotenv
from groq import Groq
import instructor
import requests

load_dotenv()


def fetch_from_web(query):
    tavily_client = TavilyClient(api_key= os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query, include_raw_content=True, max_results=10 , topic="news" , search_depth="basic")
    return {"sources": response['results']}

class Sentiment(BaseModel):
    summary: str
    reasoning: str
    topics: list[str]
    sentiment: Literal['positive', 'negative', 'neutral']

def analyze_sentiment(article , model_provider):
    
    sentiment_prompt = f"""
                Analyze the following news article about a company:

                1. **Summary**: Provide a comprehensive summary of the article's key points.
                
                2. **Sentiment Analysis**: 
                - Classify the overall sentiment toward the company as: POSITIVE, NEGATIVE, or NEUTRAL
                - Support your classification with specific quotes, tone analysis, and factual evidence from the article
                - Explain your reasoning for this sentiment classification in 2 to 3 lines.
                
                3. **Key Topics**: 
                - Identify 3-5 main topics discussed in the article
                - Only give the name of the topics

                Be as detailed and objective as possible in your reasoning.

                Article Title: {article['title']}

                Article: {article['raw_content']}
                """

    try:
        if model_provider == "Ollama":
            
            response = chat(
            messages=[
                {
                    'role': 'user',
                    'content': sentiment_prompt
                }
            ],
            model='llama3.2:3b',
            format=Sentiment.model_json_schema(),
            )

            sentiment_output = Sentiment.model_validate_json(response.message.content)
            
            final_dict = {
            "title": article["title"],
            "summary": sentiment_output.summary,
            "reasoning": sentiment_output.reasoning,
            "topics": sentiment_output.topics,
            "sentiment": sentiment_output.sentiment
        }

        else:
        
            llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            llm = instructor.from_groq(llm, mode=instructor.Mode.TOOLS)

            resp = llm.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": sentiment_prompt,
                    }
                ],
                response_model=Sentiment,
            )
        
            sentiment_output = resp.model_dump()
            
            final_dict = {
            "title": article["title"],
            "summary": sentiment_output.get("summary"),
            "reasoning": sentiment_output.get("reasoning"),
            "topics": sentiment_output.get("topics"),
            "sentiment": sentiment_output.get("sentiment")
        }

        return final_dict

    except Exception as e:
        print(f"Error parsing sentiment output: {e}")
        return None
    
def generate_comparative_sentiment(articles):

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    
    for article in articles:
        sentiment = article.get("sentiment", "").lower()
        if sentiment == "positive":
            sentiment_counts["Positive"] += 1
        elif sentiment == "negative":
            sentiment_counts["Negative"] += 1
        elif sentiment == "neutral":
            sentiment_counts["Neutral"] += 1
    
    all_topics = []
    for article in articles:
        all_topics.extend(article.get("topics", []))
    
    unique_topics = set(all_topics)
    
    topic_counts = {}
    
    for topic in unique_topics:
        count = all_topics.count(topic)
        topic_counts[topic] = count

    common_topics = [topic for topic, count in topic_counts.items() if count > 1]
    unique_topics = {}
    
    for i, article in enumerate(articles):
        article_topics = set(article.get("topics", []))
        for j, other_article in enumerate(articles):
            if i != j:
                other_topics = set(other_article.get("topics", []))
                unique_topics[f"Unique Topics in Article {i+1}"] = list(article_topics - other_topics)
    
    positive_count = sentiment_counts["Positive"]
    negative_count = sentiment_counts["Negative"]
    neutral_count = sentiment_counts["Neutral"]
    
    comparative_sentiment = {
        "Sentiment Distribution": sentiment_counts,
        "Coverage Differences": "coverage_differences",
        "Topic Overlap": {
            "Common Topics": common_topics,
            "Unique Topics in Article 1": unique_topics.get("Unique Topics in Article 1", []),
            "Unique Topics in Article 2": unique_topics.get("Unique Topics in Article 2", []),
            "Unique Topics in Article 3": unique_topics.get("Unique Topics in Article 3", []),
            "Unique Topics in Article 4": unique_topics.get("Unique Topics in Article 4", []),
            "Unique Topics in Article 5": unique_topics.get("Unique Topics in Article 5", []),
            "Unique Topics in Article 6": unique_topics.get("Unique Topics in Article 6", []),
            "Unique Topics in Article 7": unique_topics.get("Unique Topics in Article 7", []),
            "Unique Topics in Article 8": unique_topics.get("Unique Topics in Article 8", []),
            "Unique Topics in Article 9": unique_topics.get("Unique Topics in Article 9", []),
            "Unique Topics in Article 10": unique_topics.get("Unique Topics in Article 10", [])
        },
    }
    
    return comparative_sentiment

def get_summaries_by_sentiment(articles):
    pos_sum = []
    neg_sum = []
    neutral_sum = []
    
    for article in articles:

        sentiment = article.get("sentiment", "").lower()
        title = article.get("title", "No Title")
        summary = article.get("summary", "No Summary")
        
        article_text = f'Title: {title}\nSummary: {summary}'
        
        if sentiment == "positive":
            pos_sum.append(article_text)
        elif sentiment == "negative":
            neg_sum.append(article_text)
        elif sentiment == "neutral":
            neutral_sum.append(article_text)

    pos_sum = "\n\n".join(pos_sum) if pos_sum else "No positive articles available."
    neg_sum = "\n\n".join(neg_sum) if neg_sum else "No negative articles available."
    neutral_sum = "\n\n".join(neutral_sum) if neutral_sum else "No neutral articles available."

    return pos_sum , neg_sum , neutral_sum

def comparative_analysis(pos_sum , neg_sum , neutral_sum , model_provider):
    
    prompt = f"""
Perform a detailed comparative analysis of the sentiment across three categories of articles (Positive, Negative, and Neutral) about a specific company. Address the following aspects:

1. **Sentiment Breakdown**: Identify how each category (positive, negative, and neutral) portrays the company. Highlight the language, tone, and emotional cues that shape the sentiment.

2. **Key Themes and Topics**: Compare the primary themes and narratives within each sentiment group. What aspects of the company's operations, performance, or reputation does each category focus on?

3. **Perceived Company Image**: Analyze how each sentiment type influences public perception of the company. What impression is created by positive vs. negative vs. neutral coverage?

4. **Bias and Framing**: Evaluate whether any of the articles reflect explicit biases or specific agendas regarding the company. Are there patterns in how the company is framed across different sentiments?

5. **Market or Stakeholder Impact**: Discuss potential effects on stakeholders (e.g., investors, customers, regulators) based on the sentiment of each article type.

6. **Comparative Insights**: Provide a concise summary of the major differences and commonalities between the three sentiment groups. What overall narrative emerges about the company?

### Positive Articles:
{pos_sum}

### Negative Articles:
{neg_sum}

### Neutral Articles:
{neutral_sum}
"""

    if model_provider == "Ollama":

        response = chat(
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        model='llama3.2:3b'
    )
        response = response.message.content
    
    else:
        llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        chat_completion = llm.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt[:5000],
            }
        ],
        model="llama-3.3-70b-versatile",
    )
        response = chat_completion.choices[0].message.content
    
    return response

def generate_final_report(pos_sum, neg_sum, neutral_sum, comparative_sentiment , model_provider):
    final_report_prompt = f"""
    Corporate News Sentiment Analysis Report:

### 1. Executive Summary
- Overview of sentiment distribution: {comparative_sentiment["Sentiment Distribution"]['Positive']} positive, {comparative_sentiment["Sentiment Distribution"]['Negative']} negative, {comparative_sentiment["Sentiment Distribution"]['Neutral']} neutral.
- Highlight the dominant narrative shaping the company's perception.
- Summarize key drivers behind positive and negative sentiments.

### 2. Media Coverage Analysis
- Identify major news sources covering the company.
- Highlight patterns in coverage across platforms (e.g., frequency, timing).
- Identify whether media sentiment shifts over time.

### 3. Sentiment Breakdown
- **Positive Sentiment:**
    * Titles and sources: {pos_sum}
    * Key themes, notable quotes, and focal areas (e.g., product, leadership).
- **Negative Sentiment:**
    * Titles and sources: {neg_sum}
    * Key themes, notable quotes, and areas of concern.
- **Neutral Sentiment:**
    * Titles and sources: {neutral_sum}
    * Key themes and neutral narratives.

### 4. Narrative Analysis
- Identify primary storylines about the company.
- Analyze how the company is positioned (positive, neutral, negative).
- Detect shifts or emerging narratives over time.

### 5. Key Drivers of Sentiment
- Identify specific events, announcements, or actions driving media sentiment.
- Evaluate sentiment linked to industry trends vs. company-specific factors.
- Highlight company strengths and weaknesses based on media portrayal.

### 6. Competitive Context
- Identify competitor comparisons.
- Analyze how media sentiment about the company compares to industry standards.
- Highlight competitive advantages or concerns raised by the media.

### 7. Stakeholder Perspective
- Identify how key stakeholders (e.g., investors, customers, regulators) are represented.
- Analyze stakeholder concerns and reputation risks/opportunities.

### 8. Recommendations
- Suggest strategies to mitigate negative sentiment.
- Recommend approaches to amplify positive narratives.
- Provide messaging suggestions for future announcements.

### 9. Appendix
- Full article details (title, publication, date, author, URL).
- Sentiment scoring methodology.
- Media monitoring metrics (reach, engagement, etc.).
"""

    if model_provider == "Ollama":

        final_report = chat(
            messages=[
                {
                    'role': 'user',
                    'content': final_report_prompt
                }
            ],
            model='llama3.2:3b'
        )
        response = final_report.message.content
    
    else:
    
        llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        chat_completion = llm.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": final_report_prompt[:5000],
        }
    ],
    model="llama-3.3-70b-versatile",
)
        response = chat_completion.choices[0].message.content
    
    return response
    

def translate(report , model_provider):
    translation_prompt = f"""
    Translate the following corporate sentiment analysis report into Hindi:

    {report}

    Ensure the translation maintains professional tone and structure while accurately conveying key insights and details.
    """
    if model_provider == "Ollama":
    
        translation = chat(
            messages=[
                {
                    'role': 'user',
                    'content': translation_prompt
                }
            ],
            model='llama3.2:3b'
        )
        response = translation.message.content
        
    
    else:
        translation_llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        chat_completion = translation_llm.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": translation_prompt[:5000],
            }
        ],
        model="llama-3.3-70b-versatile",
    )
        response = chat_completion.choices[0].message.content
        
    return response

def text_to_speech(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb?output_format=mp3_44100_128"

    model_id="eleven_multilingual_v2"
    output_file="output.mp3"
    api_key = "sk_a927222500aab9665f83f078b92e833e7ec1389ee68238c0"
    
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": model_id
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to {output_file}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

