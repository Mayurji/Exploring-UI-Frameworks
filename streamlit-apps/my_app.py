import streamlit as st
import pandas as pd
import numpy as np

# """
# # My first app
# Here's our first attempt at using data to create a table:
# """

# df = pd.DataFrame({
#     "column-1": [1, 2, 4],
#     "column-2": [2, 3, 4]
# })

# df

# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))


dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)