import pandas as pd
from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="fin_roberta",
    tokenizer="fin_roberta",
    device=0
)

def analyze_sentiment(submissions_list: list) -> pd.DataFrame:
    records = []

    for text in submissions_list:
        out = sentiment_pipeline(text[:512])[0]
        records.append({
            "title": text,
            "label": out["label"],
            "score": round(out["score"], 3),
        })

    df = pd.DataFrame(records)
    df.to_csv("sentiment_analysis.csv", index=False)
    return df

