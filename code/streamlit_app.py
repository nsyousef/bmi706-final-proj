import streamlit as st
import pandas as pd
import altair as alt

# load and wrangle the data
@st.cache_data
def load_data():
    anxiety_depression_data = pd.read_csv("data/indicators_anxiety_depression.csv")
    death_counts_data = pd.read_csv("data/death_counts.csv")
    return anxiety_depression_data, death_counts_data

anxiety_depression_data, death_counts_data = load_data()

st.write("# Anxiety and Depression 2020 - 2024")

# mental health symptoms by category
st.write("## Mental Health Symptoms by Category")

st.write("## Mental Health Symptoms By State")

st.write("## Deaths of Despair and Mental Health Symptoms")
