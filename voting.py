import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import duckdb

def create_db(command):
    con=duckdb.connect(database=":memory:",read_only=False)
    con.execute(command)
    return con

def query(query):
    con.execute(query)
    df=con.fetchdf()
    return df

create_db_comm="create table votes as select * from read_csv_auto('1976-2016-president.csv');"
states=alt.topo_feature(data.us_10m.url, 'states')

# source = data.population_engineers_hurricanes.url
# st.write(source)

con=create_db(create_db_comm)

command ="""select m.state,m.year,m.party,t.votes
        from (
            select state,year,max(candidatevotes) as votes
            from votes
            group by state,year
            ) t join votes m on m.state=t.state and m.year=t.year and t.votes=m.candidatevotes
            order by m.year"""
df=query(command)
st.write(df)
con.execute("COPY votes TO 'map_infos.csv'")

# COPY make_map_table TO 'map_info.csv'
# base = alt.Chart(states,title='Votes').mark_geoshape().encode(
#     ).properties(
#         projection={'type':'albersUsa'},
#         width=500,
#         height=300
#     )
#     # Add Choropleth Layer
#     choro = alt.Chart(states).mark_geoshape(
#         fill='lightgray',
#         stroke='black'
#     ).encode(
#         alt.Color('df.votes', 
#                   type='quantitative', 
#                   scale=alt.Scale(scheme='bluegreen'),
#                   title = "Votes")
#     )
#     st.write(base+choro)