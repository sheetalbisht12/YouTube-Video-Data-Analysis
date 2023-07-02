# importing necessary dependencies
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS ,ImageColorGenerator

#set page title and content layout
st.set_page_config(page_title="Youtube Data Analysis",
                  page_icon=":bar_chart:",
                  layout="wide")

#reading the dataset
df = pd.read_csv("MaindataFile.csv")

#Main page
st.title(":bar_chart: YouTube Video Data Analysis")
st.markdown("---")

#--------SIDEBAR---------
st.sidebar.header("Please Filter Here")
st.sidebar.divider()

# channel selector
channel_name= st.sidebar.selectbox("Choose the Channel",
                                   options=df["Channel_Title"].unique())

st.sidebar.divider()
#year slider
year_selection = st.sidebar.multiselect("Select the Year",
                             options=df["Year"].unique(),
                             default=df["Year"].unique())

st.sidebar.divider()

# Filter query
df_selection = df.query("Channel_Title == @channel_name & Year == @year_selection")

#displaying dataframe on the app
#st.dataframe(df_selection)

#Best Performing Video
plot1 = px.bar(df_selection.sort_values('Views', ascending=False)[0:10],
              x='Views',
              y='Title',
              color_discrete_sequence=["#fc5858"],
              title="<b>Best Performing Video</b>"
             )

#Comments vs Views
plot2 = px.scatter(df_selection,
                   x='Comments',
                   y='Views',
                   color_discrete_sequence=["#fc5858"],
                  title="<b>Comments vs Views</b>")

col1, col2 = st.columns(2)
col1.plotly_chart(plot1, use_container_width=True)
col2.plotly_chart(plot2,use_container_width=True)

#Least Performing Video
plot3 = px.bar(df_selection.sort_values('Views', ascending=True)[0:10],
               x='Views',
               y='Title',
               color_discrete_sequence=["#fc5858"],
              title="<b>Least Performing Video</b>")

#Views vs Likes
plot4 = px.scatter(df_selection,
                   x='Likes',
                   y='Views',
                   color_discrete_sequence=["#fc5858"],
                  title="<b>Views vs Likes</b>")

st.divider()
col1, col2 = st.columns(2)
col1.plotly_chart(plot3, use_container_width=True)
col2.plotly_chart(plot4,use_container_width=True)

#Views per video
st.divider()
plot5 = px.violin(df_selection['Views'],
                  box=True,
                  color_discrete_sequence=["#fc5858"],
                  title="<b>Views Per Video (Violin Plot)</b>"
                 )
st.plotly_chart(plot5,use_container_width=True)

st.divider()

#wordcloud
comment_words = ''
stopwords = set(STOPWORDS)

df_selection['title_no_stopwords']= df_selection['Title'].apply(lambda x:[ item for item in str(x).split() if item not in stopwords])
pd.options.mode.chained_assignment = None

for val in df_selection['title_no_stopwords']:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
    
    
def plot_cloud(wordcloud):
    plt.figure(figsize=(30,20))
    plt.imshow(wordcloud)
    plt.axis("off");
    
wordcloud = WordCloud(width = 800, height = 400, random_state=1, background_color="black",colormap= 'OrRd', collocations = False).generate(all_words_str)
fig = (plot_cloud(wordcloud))
st.pyplot(fig)

st.set_option('deprecation.showPyplotGlobalUse', False)
#------Hide Streamlit Style-------
hide_st_style="""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




