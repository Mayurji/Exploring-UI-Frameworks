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

### Tip: You can also pass URL of the script

```
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
```