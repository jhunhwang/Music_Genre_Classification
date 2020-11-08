# Music_Genre_Classification (K-POP VS Western)

A complete machine learning pipeline from scraping music data to modelling a music genre classifier and deployting it.

The deployed web app is live at https://jihun-kpop-western-classifier.herokuapp.com/ .

## Project Scope
- Data Collection (Spotify API for Music Features and Genius API for Song Lyrics)
- Data Cleaning (Treating Null Values Inside the Dataset, etc.)
- Exploratory Data Analysis
- Machine Learning Modelling and Testing (Classification Model)
- Model Deployment
- Technologies Used
- Data Collection & Cleaning

  - Song Features
      - Spotipy API (For Collecting Music Features)
      - Pandas (Inserting the data into a dataframe, Dropping Duplicate Rows and Exporting the data as CSV)
  - Song Lyrics
      - Requests (Send request to Genius API for song info)
      - Googlesearch (If requests is unable to get the song info, a google search will be performed to find the link of the music in Genius.)
      - BeautifulSoup (With the URLs returned from either Requests or Googlesearch, BS will scrape the lyrics of the song.)
      - Pandas (Used to insert the lyrics into a dataframe)
- Exploratory Data Analysis
    - Pandas (Analyzing, Filtering, Summary)
    - Matplotlib, Seaborn (Visualization)
    - Statsmodels (ANOVA)
    - Scipy (Mannwhitneyu)
    - Itertools (For different Group Combinations)
    
 - Machine Learning Modelling
    - Sci-Kit Learn
    - XGBoost
    - Light GBM
    
 - Model Deployment
    - Streamlit
