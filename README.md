# Visualizing American Mental Health Trends During the COVID-19 Pandemic

Ava Harrington, Yung-Fang Tu, Nicholas Yousefi

## Overview

The purpose of this app is to allow people to visualize mental health trends during the COVID-19 pandemic.

## Link to App

https://mental-health-covid-trends.streamlit.app/

## Repo Structure

`code`: contains all code files needed to run the app
- `streamlit_app.py`: the main app interface

`data`: contains the datasets to be visualized
- `death_counts.csv`: counts of deaths due to various factors; used to get death by suicide data for our plots
- `indicators_anxiety_depression.csv`: percentage of people reporting symptoms of anxiety or depression, stratified by various factors such as state and demographics; plotted in majority of our graphs

`requirements.txt`: packages required to run the Streamlit app, and their versions

## Data Source Credits

Indicators of Anxiety and Depression dataset (`indicators_anxiety_depression.csv`) retrieved from: https://catalog.data.gov/dataset/indicators-of-anxiety-or-depression-based-on-reported-frequency-of-symptoms-during-last-7-

Suicide Counts dataset (`death_counts.csv`) retreived from: https://catalog.data.gov/dataset/monthly-counts-of-deaths-by-select-causes-2020-2021-2785a
