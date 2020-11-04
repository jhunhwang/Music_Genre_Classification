import streamlit as st
import pandas as pd 
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import data_dict
from copy import deepcopy
import requests 
from googlesearch import search
from bs4 import BeautifulSoup
from time import sleep
import math 

ACCESS_TOKEN = 'zLAsagg5TgwuJJkMsxjS8ZUAGqZnGfLyR6tkx23SxnxUValjJ0Ys77hSYinF-nl8'
pd.set_option('display.max_colwidth', 400)

# Function to scrape song lyrics based on the URL returned from the function above
def scrap_song_url(url):
    count = 0
    while(True):
        try:
            count += 1
            page = requests.get(url)
            html = BeautifulSoup(page.text, 'html.parser')
            lyrics = html.find('div', class_='lyrics').get_text()
            print(lyrics)
        except AttributeError:
            print('retrying....')
            if (count == 10):
                lyrics = 'null'
                break
        else:
            break
    return lyrics

def app():
    st.write("# Spotify Track Scraper Demo (Features, Lyrics)")
    artist_name = st.text_input('Artist / Group Name')
    music_info = deepcopy(data_dict.music_data)
    CLIENT_ID = '73e1d0f1d4884becbe88162f7aa017ae'
    CLIENT_SECRET = 'db0994f913bf4c58b5a555f8b34079d8'
    # Testing if CLIENT_ID and CLIENT_SECRET exist
    assert CLIENT_ID != None; assert CLIENT_SECRET != None
    print(f'This is your client_id: {CLIENT_ID}.\nThis is your client_secret: {CLIENT_SECRET}.')

    # Spotify API Login
    CLIENT_CREDENTIALS = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS)

    song_df = ''
    
    try:
        
        if (artist_name):
            with st.spinner('Beep Bop.. Processing Music Features Data'):
                # Feature Names
                feature_list = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'isWestern']
                temp_loop_feature = feature_list[:-1]
                result = sp.search(artist_name, type='artist', limit=1)
                artist_uri = result['artists']['items'][0]['uri']
                artist_genre = result['artists']['items'][0]['genres']
                sp_albums = sp.artist_albums(artist_uri, album_type='album')
                sp_single_ep = sp.artist_albums(artist_uri, album_type='single')
                sp_albums_sep_uri_temp = [sp_albums['items'][i]['uri'] for i in range(len(sp_albums["items"]))] + [sp_single_ep['items'][j]['uri'] for j in range(len(sp_single_ep['items']))]
                sp_albums_sep_name_temp = [sp_albums['items'][i]['name'] for i in range(len(sp_albums['items']))] + [sp_single_ep['items'][j]['name'] for j in range(len(sp_single_ep['items']))]
                sp_track_uri_temp = []
                for x, y in zip(sp_albums_sep_uri_temp, sp_albums_sep_name_temp):
                    print(x, y)
                    for j in range(len(sp.album_tracks(x)['items'])):
                        print(len(sp.album_tracks(x)['items']))
                        music_info['song_dtl']['album_name'].append(y)
                        music_info['song_dtl']['album_uri'].append(x)
                        sp_track_uri_temp.append(sp.album_tracks(x)['items'][j]['uri'])
                        music_info['song_dtl']['track_uri'].append(sp.album_tracks(x)['items'][j]['uri'])
                        music_info['song_dtl']['track_name'].append(sp.album_tracks(x)['items'][j]['name'])
                for track in sp_track_uri_temp:
                    track_af = sp.audio_features(tracks=track)
                    print(track_af)
                    try:
                        for feature in temp_loop_feature:
                            music_info['song_ftr'][feature].append(track_af[0][feature])
                        track_pop = sp.track(track)
                        music_info['song_ftr']['popularity'].append(track_pop['popularity'])
                    except:
                        for feature in feature_list:
                            music_info['song_ftr'][feature].append('null')
                        continue
                for i in range(len(sp_track_uri_temp)):
                    music_info['song_dtl']['artist_name'].append(artist_name)
                    music_info['song_dtl']['artist_uri'].append(artist_uri)
                    music_info['song_dtl']['artist_genre'].append(artist_genre)
                # Added as I went along (Always looking for better solutions)
                # To do list (Separate K-Pop and other genres so that the list above can be used.)
                kpop = ['ITZY', 'DREAMCATCHER', 'TWICE', 'BLACKPINK', 'Red Velvet', 'IZONE', 'BTS']
                western = ['Chainsmokers', 'John Denver']

                print(len(music_info['song_dtl']['artist_name']))
                for i in music_info['song_dtl']['artist_name']:
                    if i in kpop:
                        music_info['ml_classification']['isWestern'].append(0)
                    elif i in western:
                        music_info['ml_classification']['isWestern'].append(1)
                
                song_df = pd.DataFrame({'artist': music_info['song_dtl']['artist_name'],
                                    'artist_uri': music_info['song_dtl']['artist_uri'], 
                                    'artist_genre': music_info['song_dtl']['artist_genre'],
                                    'album_name': music_info['song_dtl']['album_name'],
                                    'album_uri': music_info['song_dtl']['album_uri'], 
                                    'track_name': music_info['song_dtl']['track_name'], 
                                    'track_uri': music_info['song_dtl']['track_uri'], 
                                    'danceability': music_info['song_ftr']['danceability'], 
                                    'energy': music_info['song_ftr']['energy'], 
                                    'key': music_info['song_ftr']['key'], 
                                    'loudness': music_info['song_ftr']['loudness'], 
                                    'mode': music_info['song_ftr']['mode'], 
                                    'speechiness': music_info['song_ftr']['speechiness'], 
                                    'acousticness': music_info['song_ftr']['acousticness'], 
                                    'instrumentalness': music_info['song_ftr']['instrumentalness'], 
                                    'liveness': music_info['song_ftr']['liveness'], 
                                    'valence': music_info['song_ftr']['valence'], 
                                    'tempo': music_info['song_ftr']['tempo'], 
                                    'duration_ms': music_info['song_ftr']['duration_ms'], 
                                    'popularity': music_info['song_ftr']['popularity'],
                                    'time_signature': music_info['song_ftr']['time_signature']
                                    })
            song_df = song_df.drop_duplicates(subset=['track_name', 'duration_ms', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'], keep='first')
            st.write('## Music Features Dataframe Output')
            st.write(song_df.reset_index(drop=True))
            st.success('Done!')
    except:
        st.write('## Something went wrong! Please try again :)')
    
    track_lyrics = []
    song_name = []
    lyric_dataframe = ''
    if isinstance(song_df, pd.DataFrame):
        with st.spinner('Beep Bop.. Processing Music Lyrics Data'):
            for index, row in song_df.iterrows():
                
                track_name = row.track_name
                artist_name = row.artist
                print(track_name, artist_name)

                backup_link = None
                
                query = track_name + artist_name + ' genius lyrics'
                for link in search(query, tld='co.in', num=10, stop=1, pause=2):
                    backup_link = link
                    break

                # Extract lyrics from URL if the song was found

                song_url = backup_link
                song_name.append(track_name)
                track_lyrics.append(scrap_song_url(song_url))
          
            lyric_dataframe = pd.DataFrame({"Song Name": song_name, "Song In Full Lyrics": track_lyrics})
        st.write('## Track Lyrics Dataframe Output')
        st.write(lyric_dataframe)
        st.success('Done!')
        st.balloons()