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

# mental health symptoms by state
st.write("## Mental Health Symptoms By State")

# filter data for this graph
anx_dat_by_state = anxiety_depression_data[
    (anxiety_depression_data["Group"] == "By State") & 
    (anxiety_depression_data["Indicator"] == "Symptoms of Anxiety Disorder or Depressive Disorder")
]

# setup multiselect
unique_states = anx_dat_by_state["Subgroup"].unique()
default_states = ["California", "Massachusetts"] # TODO: decide how to set the default

states = st.multiselect(label="State", options=unique_states, default=default_states)

anx_dat_by_state_subset = anx_dat_by_state[
    anx_dat_by_state["Subgroup"].isin(states)
]

# create the graph
graph_by_state = alt.Chart(anx_dat_by_state_subset).mark_line().encode(
    x = alt.X("Time Period End Date").title("Date"),
    y = alt.Y("Value").title("% Symptoms"),
    color = alt.Color("Subgroup").title("State")
).properties(
    title = "% Symptoms of Anxiety or Depression by State"
)

st.altair_chart(graph_by_state, use_container_width=True)

# mental health symptoms and deaths of despair
st.write("## Deaths of Despair and Mental Health Symptoms")
