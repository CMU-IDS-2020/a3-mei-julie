import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
import requests
import io
from vega_datasets import data

url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/racedata.csv"
s=requests.get(url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))

source1 = c.loc[c["Race"] == "Asian or Pacific Islander"]
source2 = c.loc[c["Race"] == "Black"]
source3 = c.loc[c["Race"] == "Hispanic"]
source4 = c.loc[c["Race"] == "White"]


asianchart=alt.Chart(source1).mark_area(opacity=0.5).encode(
    x="Year:Q",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[Asian] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)
st.write(asianchart)

blackchart=alt.Chart(source2).mark_area(opacity=0.5).encode(
    x="Year:Q",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[Black] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)
st.write(blackchart)

hispanicchart=alt.Chart(source3).mark_area(opacity=0.5).encode(
    x="Year:Q",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[Hispanic] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)
st.write(hispanicchart)

whitechart=alt.Chart(source4).mark_area(opacity=0.5).encode(
    x="Year:Q",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[White] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)
st.write(whitechart)
