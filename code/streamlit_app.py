import streamlit as st
import pandas as pd
import altair as alt

# load in the data
anxiety_depression_data = pd.read_csv("data/indicators_anxiety_depression.csv")
death_counts_data = pd.read_csv("data/death_counts.csv")

st.write("# Our BMI706 Project", unsafe_allow_html=True)
