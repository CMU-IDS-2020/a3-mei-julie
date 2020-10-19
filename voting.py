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

def make_map(w,h,source):
    return alt.Chart(states).mark_geoshape(stroke='lightgray',strokeWidth=1).encode(
        color=alt.Color("p_votes:Q",legend=alt.Legend(title="Percent Votes",tickCount=5),scale=alt.Scale(domain=(0.5,0.8))),
        tooltip=[alt.Tooltip('state:N',title="State"),alt.Tooltip('party:N',title="Party"),alt.Tooltip('p_votes:O',title="% Votes")]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(source, 'id', ['p_votes','party','state'])
    ).project(
        type='albersUsa'
    ).properties(
        width=w,
        height=h
    )

create_db_comm="create table votes as select * from read_csv_auto('1976-2016-president.csv');"
con=create_db(create_db_comm)

qq="""select year, sum(totalvotes) as totalvotes
        from votes
        group by year
        order by year"""
df_voteyear=query(qq)
# con.execute("COPY vote_year TO 'vote_year.csv'")
states=alt.topo_feature(data.us_10m.url, 'states')

# source = data.population_engineers_hurricanes.url
# st.write(source)
comm="""create table p_votes as select state,year,party,cast(candidatevotes as float)/cast(totalvotes as float) as perc_votes from votes"""
df=query(comm)
command ="""create table extra as (select m.state,m.year,m.party,t.votes
            from (
            select state,year,max(perc_votes) as votes
            from p_votes
            group by state,year
            ) t join p_votes m on m.state=t.state and m.year=t.year and t.votes=m.perc_votes
            order by m.state)"""
# df=query(command)
# create_db_comm="create table all_years as select * from read_csv_auto('byparty.csv');"
# con=create_db(create_db_comm)
# comm="create table yyy as select * from all_years where year=2000"
# df=query(comm)
# st.write(df)
# con.execute("COPY yyy TO '2000_rd.csv'")
states = alt.topo_feature(data.us_10m.url, 'states')
source00="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2000.csv"
source04="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2004.csv"
source08="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2008.csv"
source12 = "https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2012.csv"
source16="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2016.csv"

st.text("Who voted? A Breakdown of the Voting Population")
year_type = st.selectbox(
    "Select a year:",
    (None,2000,2004,2008,2012,2016)
)

# selector = alt.selection_single(fields=['totalvotes'])
votebars=alt.Chart(df_voteyear).mark_bar(size=30).encode(
    x=alt.X('year:O',axis=alt.Axis(title="Year")),
    y=alt.Y("totalvotes:Q",axis=alt.Axis(title="Number of Votes")),
    color=alt.condition(alt.datum.year==year_type,alt.value('chartreuse'),alt.value('lightblue'))
).properties(width=600)
st.write(votebars)

dem_type = st.selectbox(
    "Select a category:",
    ("Age", "Income", "Race")
)

if dem_type=='Age':
    st.write('age')
elif dem_type=='Income':
    st.write('income')
elif dem_type=='Race':
    st.write('race')

st.text("A Breakdown of Political Parties Across the States")
elec_year=st.slider("Year",min_value=2000,max_value=2016,step=4)
us=None
w=800
h=500
if elec_year==2000:
    us=make_map(w,h,source00)
elif elec_year==2004:
    us=make_map(w,h,source04)
elif elec_year==2008:
    us=make_map(w,h,source08)
elif elec_year==2012:
    us=make_map(w,h,source12)
elif elec_year==2016:
    us=make_map(w,h,source16)
st.write(us)

# # Compute x^2 + y^2 across a 2D grid
# x, y = np.meshgrid(range(-5, 5), range(-5, 5))
# z = x ** 2 + y ** 2

# # Convert this grid to columnar data expected by Altair
# source = pd.DataFrame({'x': x.ravel(),
#                      'y': y.ravel(),
#                      'z': z.ravel()})

# alt.Chart(source).mark_rect().encode(
#     x='x:O',
#     y='y:O',
#     color='z:Q'
# )
# if selected=='income':
#     h_map=alt.Chart(source16).mark_rect().encode(
#         x=''
#     )