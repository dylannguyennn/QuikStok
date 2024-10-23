import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

VADER_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(submission_dict):
    sentiment_dict = {
        "submission": [],
        "sentiment_score_pos": [],
        "sentiment_score_neg": [],
        "sentiment_score_neu": [],
        "sentiment_score_compound": []
    }

    for submission in submission_dict["title"].values():
        sentiment_score = VADER_analyzer.polarity_scores(submission)
        sentiment_dict["submission"].append(submission)
        sentiment_dict["sentiment_score_pos"].append(sentiment_score["pos"])
        sentiment_dict["sentiment_score_neg"].append(sentiment_score["neg"])
        sentiment_dict["sentiment_score_neu"].append(sentiment_score["neu"])
        sentiment_dict["sentiment_score_compound"].append(sentiment_score["compound"])

    sentiment_dict_df = pd.DataFrame(sentiment_dict)
    sentiment_dict_df.to_csv("sentiment_analysis.csv")
    return sentiment_dict

