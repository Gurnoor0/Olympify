#topics
# Medal Distribution -Onur Baltacı
# Number of unique events per sport - Onur Baltaci 17:00


import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import numpy as np

df_orig=pd.read_csv('athlete_events.csv')
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
df_orig2 = preprocessor.preprocess2(df_orig,region_df)

url = "http://localhost:3000/"
# url = "http://127.0.0.1:5500/Index.html"
st.sidebar.write("[Go Back](%s)" % url)
    

st.sidebar.title("Olympics Analysis")
# st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
st.sidebar.image('https://wallpapercave.com/wp/wp4216235.jpg')

user_menu = st.sidebar.radio(
    'Slect an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    # st.header("Medal Tally")
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    sport = [" ","Yes","No"]

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)
    selected_sport = st.sidebar.selectbox("Do you want Sport's-wise list?",sport)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country,selected_sport)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)


           # Discuss
    plt.figure(figsize=(15, 10))
    df_com= df_orig2.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    topc=df_com.groupby('region')['Medal'].count().nlargest(10).reset_index()
    fig = px.bar(topc,x='region',y='Medal')
    # fig = sns.barplot(x='region',y='Medal',data=topc)
    st.title('Top Countries in Olympic w.r.t Medals earned')
    st.plotly_chart(fig)

if user_menu == 'Overall Analysis':
    # st.title("Overall Analysis")
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    # country = df['region'].unique().tolist()

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    
    nations_over_time  = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time  = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time  = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No of Events over Time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


     

    st.title("Most Successful Athlete")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


    #Discuss
    top_10_countries=helper.top_countries(df)
    fig = px.bar(top_10_countries,x=top_10_countries.index,y=top_10_countries)
    st.title("Overall Participation by Country")
    st.plotly_chart(fig)


    #Discuss
    # st.title("Height Distribution of the Athletes")
    # fig,ax = plt.subplots()
    # plt.xlabel('Height')
    # plt.ylabel("Number of Participants")
    # ax.hist(df_orig.Height, bins = 20,color='orange')
    # st.pyplot(fig)

    #Discuss
    org_list = ['Age','Height','Weight']
    st.title("Number of Participation of the Athletes w.r.t various parameters")
    par = st.selectbox('Select a parameter',org_list)
    fig,ax = plt.subplots()
    plt.xlabel(par)
    plt.ylabel("Number of Participants")
    if par == 'Height':
        ax.hist(df_orig.Height,bins = 20,color='orange')
    elif par == 'Weight':
        ax.hist(df_orig.Weight, bins = 20,color='orange')
    elif par == 'Age':
        ax.hist(df_orig.Age, bins = 20,color='orange')
    st.pyplot(fig)


    


if user_menu == 'Country-wise Analysis':
    st.title('Country-wise Analysis')
    
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)
      
       #    NEEDS TO BE CORRECTED ***************************
    participation_df = helper.participation_tally(df,selected_country)
    fig2 = px.line(participation_df, x="Year", y="Athletes")
    st.title(selected_country + " Participation over the years")
    st.plotly_chart(fig2)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of "+ selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':
    st.title('Athelete-wise Analysis')


    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    # fig  = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    p=[]
    name = []
    famous_sports = ['Overall','Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    famous_sports2 = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    st.title("Distribution of Age wrt Sports")
    mdl_list = ['Gold','Silver','Bronze']
    mdl = st.selectbox("Select the medal type",mdl_list)
    spr = st.selectbox("Select a Sport",famous_sports)
    
    if spr == 'Overall':
        for sport in famous_sports2:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            if mdl == 'Gold':
                x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
            
            elif mdl == 'Silver':
                x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
            
            elif mdl == 'Bronze':
                x.append(temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna())

            name.append(sport)
        fig  = ff.create_distplot(x,name,show_hist=False,show_rug=False)
        fig.update_layout(autosize=False,width=1000,height=600)
        st.plotly_chart(fig)

    else:
        temp_df = athlete_df[athlete_df['Sport'] == spr]
        if mdl == 'Gold':
            x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
                
        elif mdl == 'Silver':
            x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
            
        elif mdl == 'Bronze':
            x.append(temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna())
        name.append(spr)
        fig  = ff.create_distplot(x,name,show_hist=False,show_rug=False)
        fig.update_layout(autosize=False,width=1000,height=600)
        st.plotly_chart(fig)

        

     
   #discuss
    fig=px.histogram(df_orig,x='Season',color='Sex',barmode='group',color_discrete_map={'M':'Orange','F':'Blue'})
    fig.update_layout(
        # title='Participation of male and female athletes in both season',
        yaxis_title='Athlete Count'
    )
    st.title("Participation of male and female athletes during Summer/Winter Olympics")
    st.plotly_chart(fig)

    st.title("Height vs Weight Distribution")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a sport',sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'],y = temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    # st.table(final)
    fig=px.line(final,x='Year',y=["Male", "Female"])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)


    #Discuss
    # st.title("Age Distribution of the Athletes")
    # fig,ax = plt.subplots()
    # plt.xlabel('Age')
    # plt.ylabel("Number of Participants")
    # ax.hist(df_orig.Age, bins = np.arange(10,80,2),color='orange')
    # st.pyplot(fig)

      #Discuss
    st.title("Medals earned by Atheltes")
    athlete_list = df['Name'].unique().tolist()
    year_list = df['Year'].unique().tolist()
    athlete_list.sort()
    athlete_list.insert(0,'Overall')
    year_list.sort()
    year_list.insert(0,'Overall')
    selected_athlete = st.sidebar.selectbox('Select a athlete',athlete_list)
    selected_year = st.sidebar.selectbox('Select a year',year_list)

    x=helper.athlete_data(df,selected_athlete,selected_year)
    st.table(x)
