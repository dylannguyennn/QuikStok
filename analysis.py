import pandas as pd
from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    device=0
)

def analyze_sentiment(submissions_list: list) -> pd.DataFrame:
    records = []
    print("Model loaded from:", sentiment_pipeline.model.name_or_path)
    print("Config id2label map:", sentiment_pipeline.model.config.id2label)

    for text in submissions_list:
        out = sentiment_pipeline(text[:512])[0]
        records.append({
            "title": text,
            "label": out["label"],
            "score": round(out["score"], 4),
        })

    df = pd.DataFrame(records)
    return df

