from openai import OpenAI
from dotenv import load_dotenv
import os

def ai_analysis(index_0_100, bucket, ticker):
    load_dotenv()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_KEY"),
    )

    system_prompt = "You are a chatbot on a financial data website. " \
    "Your job is to provide an analysis of the given stock ticker or company. " \
    "A sentiment value, index_0_100 will be provided, where 0 is considered very bearish and 100 is considered very bullish. " \
    "A sentiment bucket will also be provided to help you interpret this. " \
    "If you can, search the web for articles or sources that support the given sentiment value and interpretation. " \
    "Provide an explanation of the stock has the sentiment that it has. "

    prompt = f"The ticker is {ticker}. The sentiment score is {index_0_100}, and the sentiment bucket is {bucket}. " \
    "Provide an analysis of why the ticker has the sentiment score and bucket it is currently assigned."

    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
        {
            "role": "system", 
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
        }
        ]
    )

    return completion.choices[0].message.content
