import requests
from core.prompts import INSIGHT_PROMPT
from sklearn.ensemble import IsolationForest

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_insights(eda_summary):
    prompt = INSIGHT_PROMPT.format(summary=eda_summary)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

def correlation_matrix(df):
    return df.select_dtypes("number").corr()

def detect_anomalies(df):
    model = IsolationForest()
    df["anomaly"] = model.fit_predict(df.select_dtypes("number"))
    return df
