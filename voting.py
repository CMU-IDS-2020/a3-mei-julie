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

command ="""create table mapp as (select m.state,m.year,m.party,t.votes
        from (
            select state,year,max(candidatevotes) as votes
            from votes
            group by state,year
            ) t join votes m on m.state=t.state and m.year=t.year and t.votes=m.candidatevotes
            order by m.state)"""
df=query(command)
st.write(df)
# con.execute("COPY mapp TO 'map_info.csv'")
create_db_comm="create table all_years as select * from read_csv_auto('map_info.csv');"
con=create_db(create_db_comm)

comm="""create table year_2012 as select * from all_years
        where year=2012"""
df=query(comm)
st.write(df)
# con.execute("COPY year_2012 TO 'year_2012.csv'")
states = alt.topo_feature(data.us_10m.url, 'states')
source = "https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/year_2012.csv"
us=alt.Chart(states).mark_geoshape().encode(
    color='votes:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(source, 'id', ['votes'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300
)
st.write(us)