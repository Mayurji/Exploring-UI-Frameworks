## Getting Started with Streamlit


### Installation

```bash
pip install streamlit
```

### Basic Script for Streamlit

```
import strealit as st
import pandas as pd

df = pd.DataFrame({
    "column-1": [1, 2, 4],
    "column-2": [2, 3, 4]
})

df
```

### Run Streamlit App

```
streamlit run your_script.py [-- script args]
```

### Simple AI Apps With Streamlit: You Must Build In 2026

1. Personal RAG Assistant
2. AI Code Explainer
3. YouTube Script Generator
4. AI Data Explorer
5. Resume: Job Match Analyzer

### Tip: You can also pass URL of the script

```
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
```