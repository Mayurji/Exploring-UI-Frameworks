import pandas as pd

def basic_eda(df: pd.DataFrame):
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "describe": df.describe(include="all").to_dict()
    }
    return summary

def smart_eda(df, schema):
    eda = {}

    for col, dtype in schema.items():
        if dtype == "numeric":
            eda[col] = {
                "mean": df[col].mean(),
                "std": df[col].std(),
                "missing": df[col].isnull().sum()
            }
        elif dtype == "categorical":
            eda[col] = df[col].value_counts().to_dict()

    return eda


