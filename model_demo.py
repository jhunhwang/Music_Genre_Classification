import streamlit as st 
import pickle 
import pandas as pd 
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '73e1d0f1d4884becbe88162f7aa017ae'
CLIENT_SECRET = 'db0994f913bf4c58b5a555f8b34079d8'

CLIENT_CREDENTIALS = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS)

def app():
    st.write('# Classifying Western VS K-POP Tracks')
    artist_name = st.text_input('Please input your desired artist. [Make sure it is either Western or K-POP:)]')
    track_name = st.text_input('Please input your desired track. [Make sure it is either Western or K-POP :)]')
    search_str = artist_name + ' ' + track_name
    if (artist_name and track_name):
        try:
            track_details = sp.search(search_str, type='track', limit=1)['tracks']['items'][0]
            track_uri = track_details['uri']
            track_popularity = track_details['popularity']
            af = sp.audio_features(track_uri)[0]
            df_dict = { 'danceability': af['danceability'],
                        'energy': af['energy'], 
                        'key': af['key'], 
                        'loudness': af['loudness'], 
                        'mode': af['mode'], 
                        'speechiness': af['speechiness'], 
                        'acousticness': af['acousticness'], 
                        'instrumentalness': af['instrumentalness'], 
                        'liveness': af['liveness'], 
                        'valence': af['valence'], 
                        'tempo': af['tempo'], 
                        'duration_ms': af['duration_ms'], 
                        'popularity': track_popularity, 
                        'time_signature': af['time_signature']
                    }
            test_df = pd.DataFrame(df_dict, index=[0])
            print(f'Track URI Found: {track_uri}')
            filename = 'rf_model.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            result = loaded_model.predict(test_df)[0]
            predict_proba_df = pd.DataFrame(loaded_model.predict_proba(test_df))
            st.write(predict_proba_df.rename(columns={0: 'Probability of being a K-POP Song', 1: 'Probability of being a Western Song'}))
            if (result == 1):
                st.write('This is a Western Song! :sunglasses:')
                st.balloons()
            elif (result == 0):
                st.write('This is a K-POP Song! :sunglasses:')
                st.balloons()
        except:
            st.write('Song not found. Please input the correct artist and song. Then, press enter!')