import numpy as np
def country_year_list(df):
    years = df['Year'].unique().tolist()
    country = np.unique(df['region'].tolist())
    country = country.tolist()
    country.sort()

    years.sort()
    years.insert(0,'Overall')
    country.insert(0,'Overall')
    return years, country

def fetch_medal_tally(df,year, country):
    flag = 0
    df = df.drop_duplicates(subset=['Team', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event','NOC', 'Medal'], keep='first')

    if year=='Overall' and country == 'Overall':
        temp = df
        
    elif year!= 'Overall' and country == 'Overall':
        temp =  df[df['Year']==year]
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp =  df[df['region']==country]
    else:
        temp =  df[(df['Year']==year) & (df['region']==country)]
        
    total_medal = temp.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    if flag == 1:
        total_medal = temp.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold').reset_index()

    total_medal['total'] = total_medal['Gold'] + total_medal['Silver'] + total_medal['Bronze']


    return total_medal

def most_successful(df, sport):
    temp = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp = temp[temp['Sport']==sport]
        
    temp = temp['Name'].value_counts().reset_index()
    temp = temp.reset_index().merge(df, left_on='index', right_on='Name', how='left')
    temp = temp[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index').head(15).reset_index(drop=True)
    temp.columns = ['Name', 'Medals', 'Sport', 'Country']
    return temp

def country_medals(df, country):
    temp = df.dropna(subset=['Medal'])
    temp.drop_duplicates(subset=["Team", 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', "Medal"], inplace=True)
    if country != 'Overall':
        temp = temp[temp['region']==country]
        new_temp = temp
    temp = temp['Year'].value_counts().reset_index()
    
    temp.columns = ['Year', 'Medals']
    new_temp = new_temp.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return temp, new_temp
    

def most_successful_countrywise (df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df [temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head (15). merge (df, left_on='index', right_on='Name', how='left')[
    ['index', 'Name_x', 'Sport']].drop_duplicates ('index')
    x.rename (columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x



    
    
    


 
    
    
    

        

    
    
    

        


    
    

        