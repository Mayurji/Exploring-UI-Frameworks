import pandas as pd

def infer_schema(df: pd.DataFrame):
    schema = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            schema[col] = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            schema[col] = "datetime"
        elif df[col].nunique() < 20:
            schema[col] = "categorical"
        else:
            schema[col] = "text"

    return schema
