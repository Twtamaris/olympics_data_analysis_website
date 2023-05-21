import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import plotly.figure_factory as ff
#import plt
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('clean.csv')
medal_tally =pd.read_csv('medal_tally.csv')

st.sidebar.title("Olympics Data Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Table', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Analysis')
)
if user_menu == 'Medal Table':
    st.sidebar.header("Medal Table")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_list = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title("Overall Medal Tally of Olympics")
    elif selected_country != 'Overall' and selected_year == 'Overall':
        st.title(f"Overall Medal Tally of {selected_country}")
    elif selected_country == 'Overall' and selected_year != 'Overall':
        st.title(f"Overall Medal Tally of {selected_year}")
    else:
        st.title(f"Medal Tally of {selected_country} in {selected_year}")
    st.table(medal_list)

elif user_menu == 'Overall Analysis':
    st.title("Top Statistics")
    editions = df['Year'].unique().shape[0]  - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    #convert csv to dataframe
    list1 = ['csv/country_per_year.csv','csv/athletes_per_year.csv', 'csv/events_per_year.csv']
    dict1 = {'Countries participating  over the years': 
        ['Year', 'Country'], 
        'Number of athletes participating over the years': 
            ['Year', 'Name'], 
            'Number of events happened over the years': 
                ['Year', 'Events']}
    country_per_year = pd.read_csv('csv/country_per_year.csv')
    
    for i,(key, value) in enumerate(dict1.items()):
        
        data = pd.read_csv(list1[i])
        fig = px.line(data, x=value[0], y=value[1])
        st.title(key)
        st.plotly_chart(fig)

    st.title("No of Events over time")
    fig, ax = plt.subplots(figsize=(15, 15))
    x = df.drop_duplicates(['Year','Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    
    selected_sport = st.selectbox("Select Sport", sport_list)

    temp = helper.most_successful(df, selected_sport)
    st.table(temp)
    
    
    
elif user_menu == 'Country Wise Analysis':
    sport_list = df['region'].unique().tolist()
    st.sidebar.title("Country Wise Analysis")
    selected_country = st.sidebar.selectbox("Select Country", sport_list)
    st.title(f"{selected_country} with medals over Years")
    
    temp, pt = helper.country_medals(df, selected_country)
    temp.sort_values('Year', inplace=True, ascending=False)
    temp.reset_index(inplace=True)
    temp = temp.drop('index', axis=1)
    fig = px.line(temp, x="Year", y="Medals")
    st.plotly_chart(fig)
    
    
    st.title(f"Heatmap of {selected_country} with Medals Over Years")
    fig, ax = plt.subplots(figsize=(15, 15))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athlete"+ selected_country) 
    top10_df =  helper.most_successful_countrywise (df, selected_country)
    st.table(top10_df)
    
    
elif user_menu=='Athlete Analysis':
    athlete_df = df.drop_duplicates (subset=['Name', 'region'])
    x1 = athlete_df ['Age'].dropna ()
    x2 = athlete_df [athlete_df[ 'Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df [athlete_df [ 'Medal'] == 'Silver']['Age'].dropna ()
    x4 = athlete_df [athlete_df [ 'Medal'] == 'Bronze']['Age'].dropna ()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist',
    'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout (autosize=False, width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig )
    
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
    'Water Polo', 'Hockey', 'Rowing', 'Fencing',
    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery',
    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
    'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df =  athlete_df [athlete_df['Sport'] == sport] 
        x.append(temp_df [temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
        
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout (autosize=False, width=1000,height=600)
    st.title("Distribution of Age for Famous Sports")
    st.plotly_chart(fig )
        
    

    

    


    
    
    


    
 

