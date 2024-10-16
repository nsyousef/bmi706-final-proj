import streamlit as st
import pandas as pd
import altair as alt
alt.data_transformers.disable_max_rows() # allow more than 5000 rows

# load and wrangle the data
@st.cache_data
def load_data():
    # import data
    anxiety_depression_data = pd.read_csv("data/indicators_anxiety_depression.csv")
    death_counts_data = pd.read_csv("data/death_counts.csv")

    # data wrangling
    # convert dates to date type
    anxiety_depression_data["Time Period Start Date"] = pd.to_datetime(anxiety_depression_data["Time Period Start Date"], format="%m/%d/%Y")
    anxiety_depression_data["Time Period End Date"] = pd.to_datetime(anxiety_depression_data["Time Period End Date"], format="%m/%d/%Y")

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
].sort_values(by = ["Subgroup", "Time Period End Date"])

# setup multiselect
unique_states = anx_dat_by_state["Subgroup"].unique()
default_states = ["California", "Massachusetts"] # TODO: decide how to set the default

states = st.multiselect(label="States", options=unique_states, default=default_states)

anx_dat_by_state_subset = anx_dat_by_state[
    anx_dat_by_state["Subgroup"].isin(states)
]

# create the graph

# base graph containing properties common to both
xlabel = "Date"
graph_by_state_base = alt.Chart(anx_dat_by_state_subset).encode(
    x = alt.X("Time Period End Date").title(xlabel),
    y = alt.Y("Value").title("% Symptoms"),
    color = alt.Color("Subgroup").title("State"),
    tooltip=alt.value(None)
).properties(
    title = "% Symptoms of Anxiety or Depression by State"
)

# create brush to interact with state graph
state_graph_brush = alt.selection_interval(encodings = ['x'])

# upper graph shows data in detail
graph_by_state_upper = graph_by_state_base.mark_line(point=True).encode(
    x = alt.X("Time Period End Date", scale=alt.Scale(domain = state_graph_brush)).title(xlabel),
    tooltip=[
        alt.Tooltip("Time Period End Date", title="Date"), 
        alt.Tooltip("Subgroup", title="State"), 
        alt.Tooltip("Value", title="% Symptoms")
    ]
)

# lower graph gives a general overview and can be used to filter upper graph
graph_by_state_lower = graph_by_state_base.mark_line().add_params(state_graph_brush).properties(
    height = 50
)

# combine and display graphs
graph_by_state = graph_by_state_upper & graph_by_state_lower
st.altair_chart(graph_by_state, use_container_width=True)

# mental health symptoms and deaths of despair
st.write("## Deaths of Despair and Mental Health Symptoms")
