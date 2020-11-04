import streamlit as st
import images

def app():
    st.write("""
    # Music Genre Classification 
    *Github Link*: https://github.com/jhunhwang/Music_Genre_Classification

    This is my personal project on classifying **K-Pop** and **Western** Songs/Tracks.
    """)
    st.write('*Below is an infographic of the summary of the ML pipeline.*')
    st.image(images.main_page_image, use_column_width=True)

    st.write("""
    ## Project Scope

    1. Data Collection (**Spotify** API for Music Features and **Genius** API for Song Lyrics)
    2. Data Cleaning (Treating Null Values Inside the Dataset, etc.)
    3. Exploratory Data Analysis
    4. Machine Learning Modelling and Testing (**Classification** Model)
    5. Model Deployment 

    ## Technologies Used

    - **Data Collection & Cleaning**
        - **Song Features**
            - **Spotipy** API (For Collecting Music Features)
            - **Pandas** (Inserting the data into a dataframe, Dropping Duplicate Rows and Exporting the data as CSV)
        - **Song Lyrics**
            - **Requests** (Send request to Genius API for song info)
            - **Googlesearch** (If requests is unable to get the song info, a google search will be performed to find the link of the music in Genius.)
            - **BeautifulSoup** (With the URLs returned from either Requests or Googlesearch, BS will scrape the lyrics of the song.)
            - **Pandas** (Used to insert the lyrics into a dataframe)

    - **Exploratory Data Analysis**
        - **Pandas** (Analyzing, Filtering, Summary)
        - **Matplotlib, Seaborn** (Visualization)
        - **Statsmodels** (ANOVA)
        - **Scipy** (Mannwhitneyu)
        - **Itertools** (For different Group Combinations)

    - **Machine Learning Modelling**
        - **Sci-Kit Learn**
        - **XGBoost**
        - **Light GBM**

    - **Model Deployment**
        - **Streamlit**
    """)

    st.header("""Done by **Hwang Jihun**""")

