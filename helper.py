import numpy as np

# def medal_tally(df):
    # medal_tally=df.drop_duplicates(subset=['Team','NOC','Event','City','Games','Year','Medal','Sport'])
    # medal_tally=medal_tally.groupby('Region').sum()[['Gold','Silver','Bronze']].sort_values(
    #     'Gold' ,ascending=False).reset_index()
    
    # medal_tally['Total']=medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    # medal_tally['Total']= medal_tally['Total'].astype('int')
    # medal_tally['Gold']= medal_tally['Gold'].astype('int')
    # medal_tally['Silver']= medal_tally['Silver'].astype('int')
    # medal_tally['Bronze']= medal_tally['Bronze'].astype('int')
    
    # return medal_tally

def country_year_list(df):
    year=df['Year'].unique().tolist()
    year.sort()
    year.insert(0,'Overall')
    
    country=np.unique(df['Region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    
    return year,country

def fetch_medal_tally(df,year,country):
    flag=0
    medal_df=df.drop_duplicates(subset=['Team','NOC','Event','City','Games','Year','Medal'])
    # medal_df['Year']=medal_df['Year'].astype('str')
    
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    elif year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['Region']==country]
    elif year != 'Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==year]
    else:
        temp_df=medal_df[medal_df['Region']==country]
        temp_df=temp_df[temp_df['Year']==year]
    if(flag):
        medal_tally=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        medal_tally=temp_df.groupby('Region').sum()[['Gold','Silver','Bronze']].sort_values('Gold' ,ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    
    medal_tally['Total']= medal_tally['Total'].astype('int')
    medal_tally['Gold']= medal_tally['Gold'].astype('int')
    medal_tally['Silver']= medal_tally['Silver'].astype('int')
    medal_tally['Bronze']= medal_tally['Bronze'].astype('int')
#     print(x)
    return medal_tally

def data_over_time(df,col,y_name):
    data_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    data_over_time.rename(columns={'index':'Edition','Year':y_name},inplace=True)
    return data_over_time

def most_succesful(df,sport):
    temp_df=df
    temp_df=temp_df.dropna(subset=['Medal'])
    if(sport!='Overall'):
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index()
    x=x.merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','Region']].drop_duplicates()
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    if(sport!='Overall'):
        x=x[x['Sport']==sport]
    x=x.head(15)
    return x

def yearwise_medalTally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['Region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['Region']==country]
    final_df=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return final_df

def most_succesful_countrywise(df,country):
    temp_df=df
    temp_df=temp_df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['Region']==country]
    x=temp_df['Name'].value_counts().reset_index()
    x=x.merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates()
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    x=x.head(10)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final