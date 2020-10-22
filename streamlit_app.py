import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
# import duckdb
import requests
import io

# def create_db(command):
#     con=duckdb.connect(database=":memory:",read_only=False)
#     con.execute(command)
#     return con

# def query(query):
#     con.execute(query)
#     df=con.fetchdf()
#     return df
@st.cache  # add caching so we load the data only once
def load_data(url):
    return pd.read_csv(url)

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
def make_chart(source):
    return alt.Chart(source).transform_fold(
        ['Voted','Not Voted'],
        as_=['column','value']
    ).mark_bar(size=30).encode(
        x=alt.X('Age_Group:N',axis=alt.Axis(title="Age Group")),
        y=alt.Y("value:Q",axis=alt.Axis(title="Number of Votes")),
        color=alt.Color('column:N', title="Legend",
                scale=alt.Scale(range=['#ffcc5c','#96ceb4']))
    ).properties(width=600)

# create_db_comm="create table votes as select * from read_csv_auto('2000-2016-president.csv');"
# con=create_db(create_db_comm)

# qq="""create table vote_year as select year, sum(totalvotes) as totalvotes
#         from votes
#         group by year
#         order by year"""
# df_voteyear=query(qq)
# con.execute("COPY vote_year TO 'df_voteyear.csv'")
states=alt.topo_feature(data.us_10m.url, 'states')

# comm="""create table p_votes as select state,year,party,cast(candidatevotes as float)/cast(totalvotes as float) as perc_votes from votes"""
# df=query(comm)
# command ="""create table extra as (select m.state,m.year,m.party,t.votes
#             from (
#             select state,year,max(perc_votes) as votes
#             from p_votes
#             group by state,year
#             ) t join p_votes m on m.state=t.state and m.year=t.year and t.votes=m.perc_votes
#             order by m.state)"""
# create_db_comm="create table income_t as select * from read_csv_auto('income.csv');"
# con=create_db(create_db_comm)

elec_year=st.sidebar.slider("Toggle between election years:",min_value=2000,max_value=2016,step=4)

st.subheader("Who voted? A Breakdown of the Voting Population")

####AGE#####
url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/AgeData.csv"
s=requests.get(url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))

source1 = c.loc[c["Year"] == 2000]
source2 = c.loc[c["Year"] == 2004]
source3 = c.loc[c["Year"] == 2008]
source4 = c.loc[c["Year"] == 2012]
source5 = c.loc[c["Year"] == 2016]

year2000=make_chart(source1)

year2004=make_chart(source2)

year2008=make_chart(source3)

year2012=make_chart(source4)

year2016=make_chart(source5)

####INCOME#####
url=None
if elec_year==2000:
    url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/income2000.csv"
elif elec_year==2004:
    # comm="""create table income2004 as select * from income_t where year=2004"""
    # df_income=query(comm)
    url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/income2004.csv"
elif elec_year==2008:
    url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/income2008.csv"
elif elec_year==2012:
    url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/income2012.csv"
elif elec_year==2016:
    url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/income2016.csv"
df_income=load_data(url)

# selector = alt.selection_single(fields=['totalvotes'])
url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/df_voteyear.csv"
df_voteyear=load_data(url)
votebars=alt.Chart(df_voteyear).mark_bar(size=30).encode(
    x=alt.X('year:O',axis=alt.Axis(title="Year")),
    y=alt.Y("totalvotes:Q",axis=alt.Axis(title="Number of Votes")),
    color=alt.condition(alt.datum.year==elec_year,alt.value('chartreuse'),alt.value('lightblue'))
).properties(width=600)
st.write(votebars)

dem_type = st.selectbox(
    "Select a category:",
    ("Age", "Income", "Race")
)
#####RACE#####
url="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/racedata.csv"
s=requests.get(url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))

source1 = c.loc[c["Race"] == "Asian or Pacific Islander"]
source2 = c.loc[c["Race"] == "Black"]
source3 = c.loc[c["Race"] == "Hispanic"]
source4 = c.loc[c["Race"] == "White"]


asianchart=alt.Chart(source1).mark_area(opacity=0.5).encode(
    x="Year:O",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[Asian] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)

blackchart=alt.Chart(source2).mark_area(opacity=0.5).encode(
    x="Year:O",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[Black] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)

hispanicchart=alt.Chart(source3).mark_area(opacity=0.5).encode(
    x="Year:O",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[Hispanic] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)

whitechart=alt.Chart(source4).mark_area(opacity=0.5).encode(
    x="Year:O",
    y=alt.Y("Number_of_Votes:Q", stack=None, title='[White] Number of Votes'),
    color=alt.Color("Label:N",
            scale=alt.Scale(
                range=['#ffcc5c','#96ceb4','steelblue']))
).properties(height=300, width=500)

####WRITE GRAPHS######
if dem_type=='Age':
    if elec_year==2000:
        st.write(year2000)
    elif elec_year==2004:
        st.write(year2004)
    elif elec_year==2008:
        st.write(year2008)
    elif elec_year==2012:
        st.write(year2012)
    elif elec_year==2016:
        st.write(year2016)
elif dem_type=='Income':
    ####BINNED PLOT####
    income=None
    if elec_year==2000:
        income=alt.Chart(df_income).mark_circle(color='pink').encode(
        x=alt.X(field='test',type="nominal",title='Income',scale=alt.Scale(domain=["Under $5,000","$5,000 to $9,999","$10,000 to $14,999","$15,000 to $24,999",
                                                            "$25,000 to $34,999","$35,000 to $49,999","$50,000 to $74,999",
                                                            "$75,000 and over", "Income not reported"])),
        y=alt.Y(field='status',type='nominal',title='Status',scale=alt.Scale(domain=['not registered','registered','voted'])),
        size='# of People:Q'
        ).properties(
            width=500,
            height=350
        )
    else:
        income=alt.Chart(df_income).mark_circle(color='pink').encode(
        x=alt.X(field='test',type="nominal",title='Income',scale=alt.Scale(domain=["Under $10,000","$10,000 to $14,999","$15,000 to $19,999","$20,000 to $29,999",
                                                            "$30,000 to $39,999","$40,000 to $49,999","$50,000 to $74,999",
                                                            "$75,000 to $99,999","$100,000 to $149,999","$150,000 and over",
                                                            "Income not reported"])),
        y=alt.Y(field='status',type='nominal',title='Status',scale=alt.Scale(domain=['voted','registered','not registered'])),
        size='# of People:Q'
        ).properties(
            width=500,
            height=350
        )
    st.write(income)
elif dem_type=='Race':
    st.write(whitechart)
    st.write(blackchart)
    st.write(asianchart)
    st.write(hispanicchart)

###POLITICAL VIS####

###MAP###
states = alt.topo_feature(data.us_10m.url, 'states')
source00="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2000.csv"
source04="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2004.csv"
source08="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2008.csv"
source12 = "https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2012.csv"
source16="https://raw.githubusercontent.com/CMU-IDS-2020/a3-mei-julie/master/y_2016.csv"

st.subheader("A Breakdown of Political Parties Across the States")
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

# create_db_comm="create table votes as select * from read_csv_auto('republican.csv');"
# con=create_db(create_db_comm)
# comm="""select * from votes where state='California'"""
# df_votes=query(comm)
# # st.write(df_votes)
# # con.execute("COPY vv TO 'demo.csv'")
# base=alt.Chart(df_votes).properties(width=250,height=300)
# color_scale = alt.Scale(domain=['republican', 'democrat'],
#                         range=['#F94327', '#3668EC'])

# left = base.transform_filter(
#     alt.datum.party == 'democrat'
# ).encode(
#     y=alt.Y('year:O', axis=None),
#     x=alt.X('candidatevotes:Q', scale=alt.Scale(domain=(0,8500000)),
#             title='votes',
#             sort=alt.SortOrder('descending')),
#     color=alt.Color('party:N', scale=color_scale, legend=None)
# ).mark_bar(size=20).properties(title='Democrat')

# middle = base.encode(
#     y=alt.Y('year:O', axis=None),
#     text=alt.Text('year:Q'),
# ).mark_text().properties(width=27)

# right = base.transform_filter(
#     alt.datum.party == 'republican'
# ).encode(
#     y=alt.Y('year:O', axis=None),
#     x=alt.X('candidatevotes:Q', title='votes',scale=alt.Scale(domain=(0,8500000))),
#     color=alt.Color('party:N', scale=color_scale,legend=None)
# ).mark_bar(size=20).properties(title='Republican')

# st.write(alt.concat(left, middle, right, spacing=5))

#Florida, Michigan, Minnesota, New Hampshire, Pennsylvania
# artists = st.multiselect("Who are your favorite artists?", 
#                          ["Michael Jackson", "Elvis Presley",
#                          "Eminem", "Billy Joel", "Madonna"])