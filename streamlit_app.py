import streamlit as st

st.title("🎈 My new app")
st.write(
    " **Hello world !**"
)


import streamlit as st
import pandas as pd

st.write("Hello, what would you like our AI to predict")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

option = st.selectbox(
    "Which number do you like best?",
    df['first column']
)

if option > 2:
    st.write("The option selected is above 2")

else :
    st.write("The option selected is below or equal to 2")
