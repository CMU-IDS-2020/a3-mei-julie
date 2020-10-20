import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
import requests
import io
from vega_datasets import data

url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/AgeData.csv"
s=requests.get(url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))

source1 = c.loc[c["Year"] == 2000]
source2 = c.loc[c["Year"] == 2004]
source3 = c.loc[c["Year"] == 2008]
source4 = c.loc[c["Year"] == 2012]
source5 = c.loc[c["Year"] == 2016]
#st.write(c)
#st.write(source1)
#st.write(source2)
#st.write(source3)
#st.write(source4)
#st.write(source5)

year2000=alt.Chart(source1).transform_fold(
    ['Total_Voted','Total_Not_Voted'],
    as_=['column','value']
).mark_bar(size=30).encode(
    x=alt.X('Age_Group:N',axis=alt.Axis(title="Age Group")),
    y=alt.Y("value:Q",axis=alt.Axis(title="Number of Votes")),
    color=alt.Color('column:N',
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4']))
).properties(width=600)

year2004=alt.Chart(source2).transform_fold(
    ['Total_Voted','Total_Not_Voted'],
    as_=['column','value']
).mark_bar(size=30).encode(
    x=alt.X('Age_Group:N',axis=alt.Axis(title="Age Group")),
    y=alt.Y("value:Q",axis=alt.Axis(title="Number of Votes")),
    color=alt.Color('column:N',
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4']))
).properties(width=600)

year2008=alt.Chart(source3).transform_fold(
    ['Total_Voted','Total_Not_Voted'],
    as_=['column','value']
).mark_bar(size=30).encode(
    x=alt.X('Age_Group:N',axis=alt.Axis(title="Age Group")),
    y=alt.Y("value:Q",axis=alt.Axis(title="Number of Votes")),
    color=alt.Color('column:N',
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4']))
).properties(width=600)

year2012=alt.Chart(source4).transform_fold(
    ['Total_Voted','Total_Not_Voted'],
    as_=['column','value']
).mark_bar(size=30).encode(
    x=alt.X('Age_Group:N',axis=alt.Axis(title="Age Group")),
    y=alt.Y("value:Q",axis=alt.Axis(title="Number of Votes")),
    color=alt.Color('column:N',
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4']))
).properties(width=600)

year2016=alt.Chart(source5).transform_fold(
    ['Total_Voted','Total_Not_Voted'],
    as_=['column','value']
).mark_bar(size=30).encode(
    x=alt.X('Age_Group:N',axis=alt.Axis(title="Age Group")),
    y=alt.Y("value:Q",axis=alt.Axis(title="Number of Votes")),
    color=alt.Color('column:N',
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4']))
).properties(width=600)

st.write(year2000)
st.write(year2004)
st.write(year2008)
st.write(year2012)
st.write(year2016)
