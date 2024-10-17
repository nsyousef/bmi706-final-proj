import streamlit as st
import pandas as pd
import altair as alt

# constants
X_TITLE = "Month"
Y_TITLE = "% Reporting Symptoms"
Y_TITLE_SUICIDE = "Total Deaths by Suicide"
LEGEND_DEMO_TITLE = "Demographic Subcategory"
LEGEND_STATE_TITLE = "State"
WIDTH = 600

alt.data_transformers.disable_max_rows() # allow more than 5000 rows

##### load and wrangle the data #####
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

st.write("# Visualizing American Mental Health Trends During the COVID-19 Pandemic")

st.write("## Dataset")

st.write(
    """
    Here, we vizualize mental health data collected by the National Center for Health Statistics (NCHS) partnered with the Census Bureau. The data were collected via a survey called the Household Pulse survey. The survey asked patients to report if they had experienced symptoms of anxiety or depression over the last 7 days. The survey reports percentages of respondents reporting symptoms of anxiety or depression in the last 7 days.
    """
)

##### mental health symptoms by category #####
st.write("## Mental Health Trends By Demographics")

st.write("A plot of mental health trends by demographics. Data are binned by month and the mean percentage of survey respondents reporting symptoms for that bin is plotted.")

# wrangle data
mental_data = anxiety_depression_data.drop(columns=["Low CI", "High CI", "Confidence Interval", "Quartile Range"])
mental_data = mental_data.dropna()
mental_data.loc[:, 'end_date'] = pd.to_datetime(mental_data['Time Period End Date'])
mental_data = mental_data.loc[mental_data['State'] == 'United States']

# Selector for indicators
symptoms = mental_data['Indicator'].unique()
symptoms_dropdown = alt.binding_select(options=symptoms, name='Select Symptoms ')
symptoms_selection = alt.selection_point(fields=['Indicator'], bind=symptoms_dropdown, value=[{'Indicator': 'Symptoms of Depressive Disorder'}])

# Selector for categories
groups = mental_data['Group'].unique()
groups = [group for group in groups if group != 'By State']
category_dropdown = alt.binding_select(options=groups, name='Select Demographic ')
category_selection = alt.selection_point(fields=['Group'], bind=category_dropdown, value=[{'Group': 'By Age'}])

# Add brush
brush = alt.selection_interval(encodings=['x'])

# Base chart for line graph
line_chart = alt.Chart(mental_data).mark_line(point=True).encode(
    x=alt.X('yearmonth(end_date):T', title=X_TITLE),
    y=alt.Y('mean(Value):Q', title=Y_TITLE),
    color=alt.Color('Subgroup:N', legend=alt.Legend(title=LEGEND_DEMO_TITLE)),
    tooltip=[
        alt.Tooltip("yearmonth(end_date):T", title=X_TITLE),
        alt.Tooltip("Subgroup", title=LEGEND_DEMO_TITLE), 
        alt.Tooltip("mean(Value)", title=Y_TITLE)
    ]
).transform_filter(
    category_selection
).transform_filter(
    symptoms_selection
).properties(
    width=WIDTH,
    height=400
).add_params(
    category_selection
).add_params(
    symptoms_selection
).add_params(
    brush
).transform_filter(
    brush
)

# Base chart for bar graph
bar_chart = alt.Chart(mental_data).mark_bar().encode(
    x=alt.X('yearmonth(end_date):T', title=X_TITLE),
    y=alt.Y('mean(Value):Q', title=Y_TITLE, stack='zero'),
    color=alt.Color('Subgroup:N', legend=alt.Legend(title=LEGEND_DEMO_TITLE)),
    tooltip=[
        alt.Tooltip("yearmonth(end_date):T", title=X_TITLE),
        alt.Tooltip("Subgroup", title=LEGEND_DEMO_TITLE), 
        alt.Tooltip("mean(Value)", title=Y_TITLE)
    ]

).transform_filter(
    category_selection
).transform_filter(
    symptoms_selection
).properties(
    width=WIDTH,
    height=50
).add_params(
    category_selection
).add_params(
    symptoms_selection
).add_params(
    brush
)

# Combine charts
chart = line_chart & bar_chart

st.altair_chart(chart)


##### mental health symptoms by state #####
st.write("## Mental Health Trends By State")

st.write("A plot of mental health trends by US state. Data are binned by month and the mean percentage of survey respondents reporting symptoms of either anxiety or depression for that bin is plotted.")

# filter data for this graph
anx_dat_by_state = anxiety_depression_data[
    (anxiety_depression_data["Group"] == "By State") & 
    (anxiety_depression_data["Indicator"] == "Symptoms of Anxiety Disorder or Depressive Disorder")
].sort_values(by = ["Subgroup", "Time Period End Date"])

# setup multiselect
unique_states = anx_dat_by_state["Subgroup"].unique()

# set default states to ones with highest and lowest mean % reporting symptoms over entire time period
anx_dat_by_state_means = anx_dat_by_state.groupby("Subgroup").mean("Value").sort_values("Value")
default_states = [anx_dat_by_state_means.index.values[-1], anx_dat_by_state_means.index.values[0]]

states = st.multiselect(label="Select State(s)", options=unique_states, default=default_states)

anx_dat_by_state_subset = anx_dat_by_state[
    anx_dat_by_state["Subgroup"].isin(states)
]

# create the graph

# base graph containing properties common to both
graph_by_state_base = alt.Chart(anx_dat_by_state_subset).encode(
    x = alt.X("yearmonth(Time Period End Date)").title(X_TITLE),
    y = alt.Y("mean(Value)").title(Y_TITLE),
    color = alt.Color("Subgroup").title(LEGEND_STATE_TITLE),
    tooltip=alt.value(None)
).properties(
    width = WIDTH
)

# create brush to interact with state graph
state_graph_brush = alt.selection_interval(encodings = ['x'])

# upper graph shows data in detail
graph_by_state_upper = graph_by_state_base.mark_line(point=True).encode(
    x = alt.X("yearmonth(Time Period End Date)", scale=alt.Scale(domain = state_graph_brush)).title(X_TITLE),
    tooltip=[
        alt.Tooltip("yearmonth(Time Period End Date)", title=X_TITLE), 
        alt.Tooltip("Subgroup", title=LEGEND_STATE_TITLE), 
        alt.Tooltip("mean(Value)", title=Y_TITLE)
    ]
).properties(
    title = "Percentage of Respondents Reporting Symptoms of Anxiety or Depression by State"
)

# lower graph gives a general overview and can be used to filter upper graph
graph_by_state_lower = graph_by_state_base.mark_line().add_params(state_graph_brush).properties(
    height = 50
)

# combine and display graphs
graph_by_state = graph_by_state_upper & graph_by_state_lower
st.altair_chart(graph_by_state, use_container_width=True)

##### mental health symptoms and deaths of despair #####
st.write("## Mental Health Symptoms and Suicide")

st.write("A plot comparing trends in mental health symptoms with deaths by suicide from April 2020 to March 2024. The upper graph plots percentage of Household Pulse Survey respondents reporting symptoms of anxiety or depression against month. Data are binned by month, and the mean percentage of survey respondents reporting symptoms for each bin is plotted. The lower graph shows counts of deaths due to suicide per month.")

# Plotting mental health symptoms vs suicide deaths, April 2020 - March 2024

# Filter the anxiety depression data to reflect values for the USA National
# Estimates of symptoms of anxiety disorder/depressive disorder

mh_usa = anxiety_depression_data[anxiety_depression_data["State"] == "United States"]
mh_usa = mh_usa[mh_usa["Group"] == "National Estimate"] # Only look at the national estimate
mh_usa = mh_usa[mh_usa["Indicator"] == "Symptoms of Anxiety Disorder or Depressive Disorder"] # Only aggregate anx/depr symptoms
mh_usa = mh_usa.drop(columns=["Low CI", "High CI", "Confidence Interval", "Quartile Range", "Phase", "Time Period", "Indicator", "State", "Subgroup"]) # Drop unnecessary columns

mh_usa['dates'] = pd.to_datetime(mh_usa['Time Period End Date'])

mh_usa = mh_usa.dropna() # Drop NAs

# Need to do some code to turn mh_usa_final['dates'] into dates by month rather than by week

mh_usa['year'] = mh_usa['dates'].dt.year
mh_usa['month'] = mh_usa['dates'].dt.month

means = mh_usa.groupby(by=["year", "month"])['Value'].mean().reset_index()

death_counts_data['date'] = pd.to_datetime(death_counts_data['End Date'])
death_counts_data['year'] = death_counts_data["date"].dt.year
death_counts_data['month'] = death_counts_data["date"].dt.month

final = means.merge(death_counts_data, on=['year', 'month'], how="inner")

final['day'] = 1

final['date'] = pd.to_datetime(final[['year', 'month', 'day']])

final = final[final['date'] < "2023-03-01"]

# generate plot

LARGE_CHART_HEIGHT = 200

base = alt.Chart(final).properties(
    width=WIDTH
).encode(
  x=alt.X('yearmonth(date):T')
)

brush = alt.selection_interval(encodings=['x'])


upper = base.mark_line(point=True).encode(
    x=alt.X('yearmonth(date):T', title=X_TITLE).scale(domain=brush),
    y=alt.Y('Value:Q',
            title=Y_TITLE,
            scale=alt.Scale(domain=[20, 50])),
    tooltip=[
        alt.Tooltip("yearmonth(date):T", title=X_TITLE), 
        alt.Tooltip("Value:Q", title=Y_TITLE)
    ]
).properties(
    title="Percent Reporting Symptoms of Anxiety or Depression Compared to Total Deaths by Suicide",
    height = LARGE_CHART_HEIGHT
)

lower = base.mark_line(point=True).encode(
    x=alt.X('yearmonth(date):T', title=X_TITLE).scale(domain=brush),
    y=alt.Y('Intentional Self-Harm (Suicide):Q',
            title=Y_TITLE_SUICIDE,
            scale=alt.Scale(domain=[3200, 4500])),
    tooltip=[
        alt.Tooltip("yearmonth(date):T", title=X_TITLE), 
        alt.Tooltip("Intentional Self-Harm (Suicide):Q", title=Y_TITLE_SUICIDE)
    ]
    ,
    color=alt.value("#FFAA00")
).properties(
    height = LARGE_CHART_HEIGHT
)

upper2 = base.mark_line().encode(
    x=alt.X('yearmonth(date):T', title=X_TITLE),
    y=alt.Y('Value:Q',
            title=Y_TITLE),
    tooltip=alt.value(None)
)

lower2 = base.mark_line().encode(
    x=alt.X('date:T', title=X_TITLE),
    y=alt.Y('Intentional Self-Harm (Suicide):Q',
            title=Y_TITLE_SUICIDE),
    tooltip=alt.value(None),
    color=alt.value("#FFAA00")
)


layered_chart = alt.layer(upper2, lower2).resolve_scale(
    y='independent'
)

layered_chart = layered_chart.add_params(brush)

layered_chart = layered_chart.properties(
    height = 50
)

full_chart = upper & lower & layered_chart

st.altair_chart(full_chart, use_container_width=True)
